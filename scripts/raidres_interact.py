from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import os

from selenium.webdriver.firefox.options import Options as ff_opt
from selenium.webdriver.common.keys import Keys
from time import sleep


class RaidResActor():
    def __init__(self):
        self.sr_sheet_data = []
        self.active_entry = [] #sr sheet entries to compare to
        self.focused_char = [] #focused character entry on website
        self.profile_path = ""
        self.item_index = 0
        self.char_name_index = 0
        self.bonus_index = 0

        self.find_firefox_profile()

    def find_firefox_profile(self) -> str:
        if os.path.exists(os.path.join(os.environ['APPDATA'], r"Mozilla/Firefox/Profiles")):
            folder_content = os.scandir(os.path.join(os.environ['APPDATA'], r"Mozilla/Firefox/Profiles/"))
            profile_name = [file for file in folder_content if file.name.endswith(".Profil 1")]
            
            self.profile_path = os.path.join(os.environ['APPDATA'], f"Mozilla\Firefox\Profiles\{profile_name[0].name}")
        else:
            print("Need FireFox and create Profile 1")
            input("...")
            return

    def scan_sheet_data(self):
        self.active_entry = [entry for entry in self.sr_sheet_data if entry[self.char_name_index].lower() == self.focused_char[0].lower()]
        self.active_entry = [entry for entry in self.active_entry if self.focused_char[self.item_index] in entry]

    def set_sr_sheet(self,sr_sheet:list):
        self.sr_sheet_data = sr_sheet
        
        #Development might change how I format SR sheets, thats why i for charname and sr item
        self.item_index = [col_name for col_name in sr_sheet[0] if col_name.lower() == "item"][0]

        self.char_name_index = [col_name for col_name in sr_sheet[0] if col_name.lower() == "char"]
        if self.char_name_index == []:
            self.char_name_index = [col_name for col_name in sr_sheet[0] if col_name.lower() == "player"]
        self.char_name_index = self.char_name_index[0]

        self.bonus_index = [col_name for col_name in sr_sheet[0] if "bonus" in col_name.lower()][0]

        self.char_name_index = sr_sheet[0].index(self.char_name_index)
        self.item_index = sr_sheet[0].index(self.item_index)
        self.bonus_index = sr_sheet[0].index(self.bonus_index)

    def scan_site(self, site_link:str):
        firefox_opt = ff_opt()
        firefox_opt.add_argument("-profile")
        firefox_opt.add_argument(self.profile_path)
        driver =  webdriver.Firefox(options=firefox_opt)
        driver.get(site_link)

        reservation_grid = driver.find_element(By.ID, "reservations-grid")

        wait = WebDriverWait(driver, 20)
        wait.until(lambda d: len(d.find_elements(By.CSS_SELECTOR, "#reservations-grid > div")) > 1)
        sleep(2) #safety wait

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
                    except:
                        item_name = "Nothing reserved"
                        bonus_roll = "0"
                        #print(f"Char: {char_name} - SR: {item_name} - BonusRoll: {bonus_roll}")
                    else:
                        self.focused_char.clear()
                        self.focused_char = [char_name,item_name,input_field]
                        self.scan_sheet_data()
                        if self.active_entry != []:
                            self.change_entry()
                        else:
                            self.change_entry(reset=True)

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

    def change_entry(self,reset:bool=False):
        input_field = self.focused_char[2]
        input_field.click()
        input_field.send_keys(Keys.CONTROL + "a")
        input_field.send_keys(Keys.BACKSPACE)
        if reset:
            input_field.send_keys("0")
        else:
            input_field.send_keys(str(self.active_entry[0][self.bonus_index]))
