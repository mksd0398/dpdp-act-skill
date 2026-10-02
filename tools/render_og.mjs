// Render tools/og-card.html to tools/static/assets/og.jpg (1200x630, JPEG to stay under the 300 KB WhatsApp preview limit).
// Needs Playwright with Chromium:  npm i -g playwright  (or use an existing install)
import { chromium } from "playwright";
import { fileURLToPath, pathToFileURL } from "node:url";
import path from "node:path";

const here = path.dirname(fileURLToPath(import.meta.url));
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1200, height: 630 } });
await page.goto(pathToFileURL(path.join(here, "og-card.html")).href);
await page.screenshot({ path: path.join(here, "static", "assets", "og.jpg"), type: "jpeg", quality: 88 });
await browser.close();
