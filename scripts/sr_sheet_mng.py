from scripts.general_functions import get_date, color_text, print_loaded_file, order_dict_alphabetically
from scripts.file_import import load_text_file, load_json, load_csv
from scripts.export import save_json
from scripts.player_mng import PlayerManager

import os, shutil

class SrSheetManager():
    def __init__(self):
        self.__directory = load_json("./Data/_config/sr_directory")[0]["name"]
        self.__blueprint = [setting for setting in load_json("./Data/_config/config") if setting["name"] == "sr_sheet"]
        self.__sr_sheet: dict
        self.__player_dict: PlayerManager
    
    def start_sr_mng(self,player_dict:object):
        self.__player_dict = player_dict
        while True:
            menu = self.get_menu(self.__directory)
            user_input = input("option: ")
            if user_input == "0":
                print("going back...")
                break
            elif user_input == "1":
                name_input = input("SR Sheet Name: ")
                if self.__player_dict._ask_user(f"Create new SR Sheet {name_input}?"):
                    pass
                else:
                    print("canceling...")
            else:
                print("not an option")
        
    def get_menu(self,add_menu:list=[]) -> list:
        menu = ["go back\n"]
        if add_menu != []:
            menu.extend(add_menu)
        for entry in menu:
            print(f"[{menu.index(entry)}] {entry}")
        return menu