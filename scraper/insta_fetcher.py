import os
import json
from playwright.async_api import async_playwright
from config import COOKIE_FILE, IG_USERNAME, IG_PASSWORD

async def login_and_save_cookies(page):
    await page.goto("https://www.instagram.com/accounts/login/")
    await page.wait_for_timeout(5000)

    await page.fill("input[name='username']", IG_USERNAME)
    await page.fill("input[name='password']", IG_PASSWORD)
    await page.click("button[type='submit']")
    await page.wait_for_timeout(9000)

    cookies = await page.context.cookies()
    with open(COOKIE_FILE, "w") as f:
        json.dump(cookies, f)

async def load_cookies(context):
    if not os.path.exists(COOKIE_FILE):
        return False
    with open(COOKIE_FILE, "r") as f:
        cookies = json.load(f)
    await context.add_cookies(cookies)
    return True

async def get_audio_url(reel_url: str) -> str:
    async with async_playwright() as p: # automate a browser without freezing the bot.
        browser = await p.chromium.launch(headless=True) # lauch the browser in headless mode (no GUI)
        
        context = await browser.new_context() # create a new context for the browser
        
        page = await context.new_page() # create a new page for the browser

        cookies_loaded = await load_cookies(context) 
        if not cookies_loaded:
            await login_and_save_cookies(page)

        await page.goto(reel_url)
        await page.wait_for_timeout(8000)

        video = await page.query_selector("video")  # video tag from the page

        if not video:
            raise Exception("Could not find video tag")

        audio_url = await video.get_attribute("src") # get the source URL of the video
        await browser.close()
        return audio_url
