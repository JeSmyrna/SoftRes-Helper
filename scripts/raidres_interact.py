from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import os

from selenium.webdriver.firefox.options import Options as ff_opt
from selenium.webdriver.common.keys import Keys
from scripts.gsheets import get_gsheet_data
from scripts.file_import import load_csv, load_json
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
        self.__sr_directory = load_json("./Data/_config/sr_directory")[0]["name"][3:]
        self.__menu = ["going back\n", "import SR Sheet from Google Sheet", "import external local file", "import from saved raids\n", "export to RaidRes Site\n--------------------"]

        self.find_firefox_profile()

    def main(self):
        while True:
            print("--------------------")
            for opt in self.__menu:
                print(f"[{self.__menu.index(opt)}] - {opt}")

            user_entry = input("option: ")
            if user_entry == "0":
                print("closing...")
                sleep(1)
                return
            
            elif user_entry == "1":
                gsheet_link = input("Google Sheet Link: ")
                try:
                    gsheet_worksheet = int(input("Worksheet 1 -> x: ")) - 1
                except:
                    input("Input must be a number... canceling")
                else:
                    gsheet_cells = input('"From":"To" (example: "A1:B4"): ')
                    try:
                        self.sr_sheet_data = get_gsheet_data(gsheet_link,gsheet_worksheet,gsheet_cells)
                        self.set_sr_columns()
                    except:
                        print("Error: GSheet broke")
                
            elif user_entry == "2":
                file_path = input("File path (csv): ")
                if os.path.exists(file_path):
                    self.sr_sheet_data = load_csv(file_path)
                    self.set_sr_columns()
                else:
                    input("File doesn't exist. Check Path...")

            elif user_entry == "3":
                for raid in self.__sr_directory:
                    print(f"[{self.__sr_directory.index(raid)}] - {raid}")
                try:
                    raid_name = self.__sr_directory[int(input("option: "))]
                    self.sr_sheet_data = load_csv(f"./Data/{raid_name}/{raid_name}")
                    self.set_sr_columns()
                except:
                    input("Error: unexpected...")

            elif user_entry == "4":
                if self.sr_sheet_data != []:
                    hyperlink = input("Input Raidres HTML Link: ")
                    self.scan_site(hyperlink)
                else:
                    input("Need to SR sheet data... ")

            elif user_entry == "5":
                for entry in self.sr_sheet_data:
                    print(entry)
            else:
                print("not an option")

    def find_firefox_profile(self) -> str:
        try:
            if os.path.exists(os.path.join(os.environ['APPDATA'], r"Mozilla/Firefox/Profiles")):
                folder_content = os.scandir(os.path.join(os.environ['APPDATA'], r"Mozilla/Firefox/Profiles/"))
                profile_name = [file for file in folder_content if file.name.endswith(".Profil 1")]
                
                self.profile_path = os.path.join(os.environ['APPDATA'], f"Mozilla\Firefox\Profiles\{profile_name[0].name}")
            else:
                print("Need FireFox and create Profile 1")
                input("...")
                return
        except:
            print("Something went wrong, try again.")
            input("...")

    def scan_sheet_data(self):
        self.active_entry = [entry for entry in self.sr_sheet_data if entry[self.char_name_index].lower() == self.focused_char[0].lower()]
        self.active_entry = [entry for entry in self.active_entry if self.focused_char[1] in entry]

    #legacy function ?
    def set_sr_sheet(self,sr_sheet:list):
        self.sr_sheet_data = sr_sheet
        self.set_sr_columns()
        
    def set_sr_columns(self):
        #Development might change how I format SR sheets, thats why i for charname and sr item
        self.item_index = [col_name for col_name in self.sr_sheet_data[0] if col_name.lower() == "item"][0]

        self.char_name_index = [col_name for col_name in self.sr_sheet_data[0] if col_name.lower() == "char"]
        if self.char_name_index == []:
            self.char_name_index = [col_name for col_name in self.sr_sheet_data[0] if col_name.lower() == "player"]
        self.char_name_index = self.char_name_index[0]

        self.bonus_index = [col_name for col_name in self.sr_sheet_data[0] if "bonus" == col_name.lower()][0]

        self.char_name_index = self.sr_sheet_data[0].index(self.char_name_index)
        self.item_index = self.sr_sheet_data[0].index(self.item_index)
        self.bonus_index = self.sr_sheet_data[0].index(self.bonus_index)

    def scan_site(self, site_link:str):
        firefox_opt = ff_opt()
        firefox_opt.add_argument("-profile")
        firefox_opt.add_argument(self.profile_path)
        try:
            driver =  webdriver.Firefox(options=firefox_opt)
        except:
            input("Error: unexpected. Try again... ")
            return
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
                driver.close()
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
