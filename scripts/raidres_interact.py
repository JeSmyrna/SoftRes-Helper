from playwright.sync_api import sync_playwright
import os

with sync_playwright() as p:
    
    browser_context = p.chromium.launch(headless=False)
    url = "https://raidres.top/res/73c4hz"

    try:
        page = browser_context.new_page()
        page.goto(url, wait_until="networkidle")
        page.wait_for_selector("#reservations-grid")
    except:
        print("Error")

    else:
        entries = page.query_selector_all('#reservations-grid > div')
        if entries:
            for e in entries[1:]:
                name = e.query_selector('.character-name > div > button > p')
                item = e.query_selector('.raid-item > a > div > span')
                sr_plus = e.query_selector('.sr-plus > div > input')