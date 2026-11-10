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
Pages, the sitemap and the index read `getCatalog()`. The episode page calls `notFound()` when the slug isn't live.

## Cache Components gotchas
| Symptom | Fix |
|---|---|
| Build error: `dynamicParams` not compatible with `cacheComponents` | Delete it; call `notFound()` for unknown or unreleased slugs |
| An unreleased slug returns 200 with the 404 UI | Set `partialPrefetching: false` in `next.config.ts`, and await `params` outside `<Suspense>` |
| `generateStaticParams` returning `[]` errors | Return every episode slug, scheduled ones included |

## Verify
```bash
curl -s -o /dev/null -w "%{http_code}\n" https://<site>/episodes/<scheduled-slug>   # 404 before release
curl -s https://<site>/sitemap.xml | grep -c "<loc>"                                 # only live episodes
```
Video files in `public/` are reachable before release if someone guesses the URL. Accept that, or upload them on release day.
