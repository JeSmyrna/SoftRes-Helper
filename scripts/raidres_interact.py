from playwright.sync_api import sync_playwright
import os

with sync_playwright() as p:
    #profile_path = os.path.join(os.getenv('APPDATA'), r'Mozilla/Firefox/Profiles/P6ziroSq.Profil 1')
    #browser_context = p.firefox.launch(executable_path=f'C:/Program Files (x86)/Mozilla Firefox/firefox.exe', headless=False)
    #browser_context = p.firefox.launch_persistent_context(user_data_dir=profile_path, executable_path=f'C:/Program Files (x86)/Mozilla Firefox/firefox.exe', headless=False)
    #user_data_path = os.path.join(os.getenv('LOCALAPPDATA'), r'Google/Chrome/User Data')
    #browser_context = p.chromium.launch_persistent_context(headless=False, user_data_dir=user_data_path, channel='chrome', args=["--profile-directory=Profile 1"])
    browser_context = p.chromium.launch(headless=False)
    url = "https://raidres.top/res/73c4hz"

    try:
        page = browser_context.new_page()
        #page = browser_context.pages[0] if browser_context.pages else browser_context.new_page()
        page.goto(url, wait_until="networkidle")
        page.wait_for_selector("#reservations-grid")
    except:
        print("Error")

    else:
        check_rules = page.query_selector('#reservations-grid')
        if check_rules.get_attribute('data-srplus') == '1':
            if check_rules.get_attribute('data-admin') == '1':
                print("all good!")
            else:
                print("no admin rights")
                input("...")
        else:
            print("Sheet has no SR+ enabled")
            input("...")
        """ entries = page.query_selector_all('#reservations-grid > div')
        if entries:
            for e in entries[1:]:
                name = e.query_selector('.character-name > div > button > p')
                item = e.query_selector('.raid-item > a > div > span')
                sr_plus = e.query_selector('.sr-plus > div > input') """