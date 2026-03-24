from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import os

from selenium.webdriver.firefox.options import Options as ff_opt
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.common.keys import Keys
from time import sleep


profile_path = os.path.join(os.environ['APPDATA'], r"Mozilla/Firefox/Profiles/P6ziroSq.Profil 1")
ff_profile = FirefoxProfile()

firefox_opt = ff_opt()
firefox_opt.add_argument("-profile")
firefox_opt.add_argument(profile_path)
driver =  webdriver.Firefox(options=firefox_opt)
driver.get("https://raidres.top/res/73c4hz")

reservation_grid = driver.find_element(By.ID, "reservations-grid")

wait = WebDriverWait(driver, 20)
wait.until(lambda d: len(d.find_elements(By.CSS_SELECTOR, "#reservations-grid > div")) > 1)
sleep(2) #safety wait

print(reservation_grid.get_attribute("data-srplus"))
if reservation_grid.get_attribute("data-srplus") == "1":
    if reservation_grid.get_attribute("data-admin") == "1":
    
        all_entries  = reservation_grid.find_elements(By.CSS_SELECTOR, "#reservations-grid > div")

        for e in all_entries[1:]:
            char_name = e.find_element(By.CLASS_NAME, "character-name")
            char_name = char_name.text.strip()
            try:
                item_name = e.find_element(By.CLASS_NAME, "raid-item")
                item_name = item_name.text.strip()
                input_field = e.find_element(By.CSS_SELECTOR, ".sr-plus > div > input")
                bonus_roll = input_field.get_attribute("value")
                
                input_field.click()
                input_field.send_keys(Keys.CONTROL + "a")
                input_field.send_keys(Keys.BACKSPACE)
                input_field.send_keys("69")
                #input_field.send_keys(Keys.ENTER) #i think this will reload the page

            except:
                item_name = "Nothing reserved"
                bonus_roll = "0"
                print(f"Char: {char_name} - SR: {item_name} - BonusRoll: {bonus_roll}")
            else:
                print(f"Char: {char_name} - SR: {item_name} - BonusRoll: {bonus_roll}")

        input("...")
        #code to hit the save button
        all_btns = driver.find_elements(By.TAG_NAME, "button")
        for btn in all_btns:
            try:
                btn_value = btn.find_element(By.CSS_SELECTOR, "span > span")
                if btn_value.text.strip() == "Update SR+":
                    btn.click()
            except:
                pass
    else:
        print("No Admin rights")
else:
    print("SR Plus disabled")
