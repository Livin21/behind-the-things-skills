# Releasing episode pages at the scheduled time (Next.js 16)

The goal: each episode page appears at the same minute as the videos, with no redeploy and no cron.

## Data
Give every episode a `releaseAt` ISO time, for example `"2026-11-18T14:00:00Z"` for 19:30 IST. Keep all episodes, released and scheduled, in one array.

## Catalogue (cached, recomputed every minute)
```ts
// content/catalog.ts
import { cacheLife } from "next/cache";
import { allEpisodes, laterTitles } from "./episodes";

export async function getCatalog() {
  "use cache";
  cacheLife("minutes"); // revalidate about every minute; Date.now() is allowed inside a use-cache scope
  const now = Date.now();
  const live = allEpisodes.filter((e) => Date.parse(e.releaseAt) <= now).sort((a, b) => b.number - a.number);
  const scheduled = allEpisodes.filter((e) => Date.parse(e.releaseAt) > now)
    .map((e) => ({ number: e.number, thing: e.thing }));
  return { live, upcoming: [...scheduled, ...laterTitles] };
}
```
The sitemap and the index read `getCatalog()`.

## The release gate lives in `proxy.ts`, not in the page
**Don't** call `notFound()` from the episode page based on the time. Pages are prebuilt; an unreleased page is prebuilt as "not found", and after release the CDN serves that stale 404 to the first visitor (stale-while-revalidate). On L01's channel, `/episodes/barcode` returned 404 to its first visitor two and a half days after release.

Instead, the page always renders the episode (it 404s only for unknown slugs), and a proxy decides per request:
```ts
// proxy.ts (project root; Next 16 renamed middleware to proxy)
import { NextResponse, type NextRequest } from "next/server";
import { allEpisodes } from "./content/episodes";
const releaseAt = new Map(allEpisodes.map((e) => [e.slug, Date.parse(e.releaseAt)]));
export function proxy(request: NextRequest) {
  const slug = request.nextUrl.pathname.split("/")[2];
  const at = slug ? releaseAt.get(slug) : undefined;
  if (at !== undefined && at > Date.now()) return NextResponse.rewrite(new URL("/episodes/not-yet-released", request.url));
  return NextResponse.next();
}
export const config = { matcher: "/episodes/:slug" };
```
The rewrite target is a slug that doesn't exist, so the visitor gets the normal 404 page with a 404 status. Test it by setting one episode's `releaseAt` two minutes ahead, building once, and checking that the page goes 404 → 200 at that second with no rebuild.

## Cache Components gotchas
| Symptom | Fix |
|---|---|
| Build error: `dynamicParams` not compatible with `cacheComponents` | Delete it; call `notFound()` for unknown or unreleased slugs |
| An unreleased slug returns 200 with the 404 UI | Set `partialPrefetching: false` in `next.config.ts`, and await `params` outside `<Suspense>` |
| `generateStaticParams` returning `[]` errors | Return every episode slug, scheduled ones included |

## Verify
```bash
curl -s -o /dev/null -w "%{http_code}\n" https://<site>/episodes/<scheduled-slug>   # 404 before release
curl -s -o /dev/null -w "%{http_code}\n" https://<site>/episodes/<released-slug>    # 200 on the FIRST request after release
curl -s https://<site>/sitemap.xml | grep -c "<loc>"                                 # only live episodes
```
Video files in `public/` are reachable before release if someone guesses the URL. Accept that, or upload them on release day.
