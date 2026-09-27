import { chromium } from "playwright";
import fs from "node:fs/promises";
import path from "node:path";

const target = process.env.TARGET_URL || "https://josh-temple.github.io/systematic-trading-research/";
const outDir = process.env.ARTIFACT_DIR || "artifacts/mobile-web-validation";

const viewports = [
  { name: "android-360x800", width: 360, height: 800 },
  { name: "android-390x844", width: 390, height: 844 },
  { name: "android-412x915", width: 412, height: 915 },
];

const requireIncludes = (text, needle, label) => {
  if (!text.includes(needle)) {
    throw new Error(`${label}: missing text: ${needle}`);
  }
};

await fs.mkdir(outDir, { recursive: true });

const browser = await chromium.launch();
const results = [];

try {
  for (const viewport of viewports) {
    const context = await browser.newContext({
      viewport: { width: viewport.width, height: viewport.height },
      deviceScaleFactor: 1,
      isMobile: true,
      hasTouch: true,
    });
    const page = await context.newPage();

    const response = await page.goto(target, {
      waitUntil: "networkidle",
      timeout: 60_000,
    });
    if (!response || !response.ok()) {
      throw new Error(`${viewport.name}: public page response not OK`);
    }

    await page.waitForSelector("#current-status .current-row", { timeout: 15_000 });

    const title = (await page.locator("#line-title").innerText()).trim();
    if (title !== "Horizontal Reaction Strategy v0.1") {
      throw new Error(`${viewport.name}: unexpected H1 title: ${title}`);
    }

    const bodyText = await page.locator("body").innerText();
    requireIncludes(bodyText, "NOT SUPPORTED", viewport.name);
    requireIncludes(bodyText, "NO UNCONDITIONAL TOUCH SUPPORT", viewport.name);
    requireIncludes(bodyText, "WAITING FOR MATURITY", viewport.name);
    requireIncludes(bodyText, "SOURCE CONFLICT", viewport.name);
    requireIncludes(bodyText, "BLOCKED", viewport.name);
    requireIncludes(bodyText, "CONSUMED HOLDOUT", viewport.name);
    requireIncludes(bodyText, "FINAL HOLDOUT / UNUSED", viewport.name);
    requireIncludes(bodyText, "DEC-HR-004", viewport.name);

    const geometry = await page.evaluate(() => ({
      scrollWidth: document.documentElement.scrollWidth,
      clientWidth: document.documentElement.clientWidth,
      bodyScrollWidth: document.body.scrollWidth,
      currentTop: document.querySelector("#current")?.getBoundingClientRect().top ?? null,
      timelineTop: document.querySelector("#timeline")?.getBoundingClientRect().top ?? null,
    }));

    if (geometry.scrollWidth > geometry.clientWidth + 1) {
      throw new Error(
        `${viewport.name}: horizontal overflow: scrollWidth=${geometry.scrollWidth}, clientWidth=${geometry.clientWidth}`
      );
    }
    if (geometry.bodyScrollWidth > geometry.clientWidth + 1) {
      throw new Error(
        `${viewport.name}: body horizontal overflow: bodyScrollWidth=${geometry.bodyScrollWidth}, clientWidth=${geometry.clientWidth}`
      );
    }
    if (
      geometry.currentTop === null ||
      geometry.timelineTop === null ||
      geometry.currentTop >= geometry.timelineTop
    ) {
      throw new Error(`${viewport.name}: CURRENT section is not before historical timeline`);
    }

    const summaryLink = page.locator("#canonical-link");
    const summaryLabel = (await summaryLink.innerText()).trim();
    const summaryHref = await summaryLink.getAttribute("href");
    if (summaryLabel !== "Current summary ↗") {
      throw new Error(`${viewport.name}: unexpected current-summary label: ${summaryLabel}`);
    }
    if (!summaryHref?.endsWith("/research/lines/horizontal-reaction-v0.1/CURRENT.md")) {
      throw new Error(`${viewport.name}: current-summary href is wrong: ${summaryHref}`);
    }

    const popupPromise = page.waitForEvent("popup");
    await summaryLink.click();
    const popup = await popupPromise;
    await popup.waitForLoadState("domcontentloaded", { timeout: 30_000 }).catch(() => {});
    const popupUrl = popup.url();
    if (!popupUrl.includes("github.com/Josh-Temple/systematic-trading-research")) {
      throw new Error(`${viewport.name}: current-summary tap did not open GitHub: ${popupUrl}`);
    }
    await popup.close();

    const diagnosticLinks = await page.locator("#diag-links a").count();
    const timelineLinks = await page.locator("#timeline-list a").count();
    if (diagnosticLinks < 2) {
      throw new Error(`${viewport.name}: expected at least 2 diagnostic evidence links`);
    }
    if (timelineLinks < 9) {
      throw new Error(`${viewport.name}: expected canonical links for timeline records`);
    }

    const screenshotPath = path.join(outDir, `${viewport.name}.png`);
    await page.screenshot({ path: screenshotPath, fullPage: true });

    results.push({
      viewport,
      responseStatus: response.status(),
      title,
      horizontalOverflow: false,
      sourceConflictVisible: bodyText.includes("SOURCE CONFLICT"),
      blockedDistinctTextPresent: bodyText.includes("BLOCKED"),
      notSupportedDistinctTextPresent: bodyText.includes("NOT SUPPORTED"),
      consumedTextPresent: bodyText.includes("CONSUMED HOLDOUT"),
      unusedTextPresent: bodyText.includes("FINAL HOLDOUT / UNUSED"),
      currentSummaryLink: summaryHref,
      currentSummaryTapUrl: popupUrl,
      diagnosticLinks,
      timelineLinks,
      screenshot: screenshotPath,
    });

    await context.close();
  }
} finally {
  await browser.close();
}

await fs.writeFile(
  path.join(outDir, "result.json"),
  JSON.stringify(
    {
      status: "PASS",
      target,
      checkedAt: new Date().toISOString(),
      checks: results,
    },
    null,
    2
  )
);

console.log(JSON.stringify({ status: "PASS", target, checks: results }, null, 2));
