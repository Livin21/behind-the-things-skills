// Extract sound cues from a HyperFrames short by inspecting its GSAP timeline in headless Chrome.
// Usage: node extract_cues.mjs <project-dir> [out.json]   (writes <project-dir>/sfx-cues.json by default)
// Uses the Chrome that HyperFrames already downloaded (`npx hyperframes@<project pin> browser path`).
import { readFileSync, writeFileSync, existsSync, statSync } from "node:fs";
import { createServer } from "node:http";
import { join, extname, resolve, dirname } from "node:path";
import { execSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import puppeteer from "puppeteer-core";

const here = dirname(fileURLToPath(import.meta.url));
const dir = resolve(process.argv[2] || ".");
const out = process.argv[3] || join(dir, "sfx-cues.json");
const fnText = readFileSync(join(here, "extract_cues.js"), "utf8").replace(/^\s*\/\/.*$/gm, "").trim();
const types = { ".html": "text/html", ".js": "text/javascript", ".css": "text/css", ".json": "application/json", ".png": "image/png",
  ".jpg": "image/jpeg", ".svg": "image/svg+xml", ".woff2": "font/woff2", ".mp3": "audio/mpeg", ".wav": "audio/wav" };

const server = createServer((req, res) => {
  const p = join(dir, decodeURIComponent(req.url.split("?")[0]).replace(/^\/+/, "") || "index.html");
  if (!p.startsWith(dir) || !existsSync(p) || statSync(p).isDirectory()) { res.writeHead(404); return res.end(); }
  res.writeHead(200, { "content-type": types[extname(p)] || "application/octet-stream" }); res.end(readFileSync(p));
}).listen(0);
const port = server.address().port;
let pin = "0.9.28";
try { const pk = JSON.parse(readFileSync(join(dir, "package.json"), "utf8")); const v = (pk.dependencies || {}).hyperframes || (pk.devDependencies || {}).hyperframes; if (v) pin = v.replace(/^[^\d]*/, ""); } catch {}
const chrome = execSync(`npx --yes hyperframes@${pin} browser path`, { encoding: "utf8", stdio: ["ignore", "pipe", "ignore"] }).trim().split("\n").pop();
const browser = await puppeteer.launch({ executablePath: chrome, headless: true, args: ["--autoplay-policy=no-user-gesture-required"] });
try {
  const page = await browser.newPage();
  const errs = [];
  page.on("pageerror", (e) => errs.push("pageerror: " + e.message));
  page.on("console", (m) => { if (m.type() === "error") errs.push("console: " + m.text()); });
  page.on("requestfailed", (r) => errs.push("failed: " + r.url().slice(0, 120)));
  await page.goto(`http://127.0.0.1:${port}/index.html`, { waitUntil: "load", timeout: 60000 });
  // Poll by hand: headless-shell doesn't run rAF/MutationObserver-based waits reliably.
  let state = null;
  for (let i = 0; i < 60; i++) {
    state = await page.evaluate(() => ({ ready: document.readyState, title: document.title, tl: window.__timelines ? Object.keys(window.__timelines) : null }));
    if (state.tl && state.tl.includes("main")) break;
    await new Promise((r) => setTimeout(r, 500));
  }
  if (!state.tl || !state.tl.includes("main")) { console.error(JSON.stringify(state), errs.join("\n")); throw new Error("timeline 'main' never appeared"); }
  const cues = await page.evaluate(`(${fnText})()`);
  if (!Array.isArray(cues)) throw new Error("extractor failed: " + JSON.stringify(cues));
  const dur = await page.evaluate(() => window.__timelines.main.duration());
  writeFileSync(out, JSON.stringify({ n: cues.length, dur, cues }, null, 1));
  const ticks = cues.filter((c) => c.s.startsWith("digit")).length;
  console.log(`${out}: ${cues.length} cues over ${dur.toFixed(1)} s; ${((cues.length - ticks) / dur).toFixed(2)}/s without counter ticks (${ticks} digit ticks)`);
} finally {
  await browser.close(); server.close();
}
