from scripts.general_functions import get_date, color_text, print_loaded_file, order_dict_alphabetically, print_menu_title
from scripts.file_import import load_text_file, load_json, load_csv
from scripts.export import save_json, save_csv
from scripts.player_mng import PlayerManager

import os, shutil
from time import sleep

class SrSheetManager():
    def __init__(self):
        self.__directory = load_json("./Data/_config/sr_directory")[0]["name"]
        self.__blueprint = [setting for setting in load_json("./Data/_config/config") if setting["name"] == "sr_sheet"][0]
        self.__sr_sheet: dict
        self.__player_dict: PlayerManager
    
    def start_sr_mng(self,player_dict:object):
        self.__player_dict = player_dict
        while True:
            print(chr(27) + "[2J") #clear terminal
            self.get_menu(self.__directory)
            user_input = input("option: ")
            if user_input == "0":
                print("going back...")
                break
            elif user_input == "1":
                name_input = input("SR Sheet Name: ")
                if self.__player_dict._ask_user(f"Create new SR Sheet {name_input}?"):
                    self._create_new_sr_sheet(name_input)
                else:
                    print("canceling...")
                    sleep(1)
            elif user_input == "2":
                if len(self.__directory) > 3:
                    print_menu_title("Delete SR Sheet")
                    self.get_menu(self.__directory[3:])
                    menu = self.__directory[3:]
                    user_input = input("option: ")
                    try:
                        sr_sheet = menu[int(user_input)]
                        self._delete_sr_sheet(sr_sheet)
                    except:
                        print("invalid input")
                        sleep(1)
                else:
                    print("no SR sheet detected.")
                    sleep(1)
        
    def get_menu(self,menu:list=[]):
        for entry in menu:
            print(f"[{menu.index(entry)}] {entry}")
    
    def save_sr_directory(self):
        save_json("./Data/_config/sr_directory", [{"name":self.__directory}])

    def _delete_sr_sheet(self,sr_name:str):
        if os.path.exists(f"./Data/{sr_name}/"):
            if self.__player_dict._ask_user(f"Are your you want to {color_text(f"delete the whole folder of {sr_name}?","rd")}\n{color_text("This can't be reversed","yw")}"):
                shutil.rmtree(f"./Data/{sr_name}/")
                self.__directory.remove(sr_name)
                self.save_sr_directory()
                print("successfully deleted directory")
                sleep(1)
            else:
                print("going back...")
                sleep(1)
        else:
            print("SR Sheet doesn't exist")
            sleep(1)

    def _create_new_sr_sheet(self,raidname:str):

        if os.path.exists(f"./Data/{raidname}"):
            print("already exists")
        else:
            self.__directory.append(raidname)
            self.save_sr_directory()

            new_path = f"./Data/{raidname}/"
            os.mkdir(new_path)

            os.mkdir(f"{new_path}logs/")
            os.mkdir(f"{new_path}sr_saves/")
            os.mkdir(f"{new_path}sr_saves/sr_sheets/")
            os.mkdir(f"{new_path}sr_saves/sr_awarded/")

            save_json(f"{new_path}settings",[self.__blueprint["settings"]])
            save_csv(f"{new_path}{raidname}",[self.__blueprint["columns"]])
            save_csv(f"{new_path}sr_awarded",[self.__blueprint["awarded"]])