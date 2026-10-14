"""Headless screenshots of the site for visual QA: python scripts/screenshot.py URL OUT.png [width height] [wait_ms] [click_selector ...]"""
import sys, asyncio, os
os.environ.setdefault("PLAYWRIGHT_BROWSERS_PATH", "/mnt/hdd2/Abhijit/.cache/ms-playwright")
from playwright.async_api import async_playwright
async def main(url, out, w=1440, h=900, wait=6000, clicks=()):
    async with async_playwright() as p:
        b = await p.chromium.launch(args=["--no-sandbox"]); pg = await b.new_page(viewport={"width": int(w), "height": int(h)}, device_scale_factor=1)
        logs = []; pg.on("console", lambda m: logs.append(f"{m.type}: {m.text}")); pg.on("pageerror", lambda e: logs.append(f"pageerror: {e}"))
        await pg.goto(url, wait_until="networkidle"); await pg.wait_for_timeout(int(wait))
        for sel in clicks:
            await pg.click(sel); await pg.wait_for_timeout(2500)
        await pg.screenshot(path=out, full_page=True); await b.close()
        print("\n".join(logs[-15:])); print("saved", out)
a = sys.argv[1:]; asyncio.run(main(a[0], a[1], *(a[2:4] or [1440, 900]), *(a[4:5] or [6000]), clicks=a[5:]))
