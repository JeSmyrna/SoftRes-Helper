from scripts.file_import import load_json
from scripts.export import save_json
from scripts.general_functions import color_text

from time import sleep

class PlayerManager():
    def __init__(self):
        self.__player_dict = []
        self.__print_config = [settings for settings in load_json("./Data/_config/config") if settings["name"] == "col_lengths"][0]
        self.__classes = list([classes for classes in load_json("./Data/_config/config") if classes["name"] == "class_color"][0].keys())
        self.load_player_dict()

    def load_player_dict(self):
        self.__player_dict = load_json("./Data/_config/player_dict")

    def save_player_dict(self):
        save_json("./Data/_config/player_dict",self.__player_dict)

    def _ask_user(self, warning_text:str="Are you sure?"):
        while True:
            ask_user = input(f"{warning_text} (y/n): ")
            if ask_user == "y":
                return True
            elif ask_user == "n":
                return False
            else:
                print("-"*10)
                
    def choose_class(self) -> str:
        while True:
            for option in self.__classes[1:]:
                print(f"[{self.__classes.index(option)}] {option}")
            print("-"*20)
            user_entry = input("option: ")
            if user_entry == "0":
                print("returning...")
                sleep(1)
                return
            try:
                return self.__classes[int(user_entry)]
            except:
                print(f"input needs to be a number from 0 - {len(self.__classes)}")

    def add_player(self,player:dict):
        """
        player = {'name','class','owner'}
        """
        if self.get_chars_of_player(player["name"],False) == []:
            if self.get_chars_of_player(player["owner"]) == []:
                print(f"Owner {color_text(player["owner"],"yw")} does not exist")
            else:
                self.__player_dict.append(player)
                self.sort_players()
                self.save_player_dict()
        else:
            print("Character already exists")

    def delete_player(self,name:str="",del_all:bool=False):
        if name == "":
            print("nothing to delete")
        else:
            new_player_dict = []
            dict_changed = False
            if del_all:
                if self.get_chars_of_player(name) == []:
                    print("Character owner not found.")
                else:
                    self.print_chars(name,True)
                    if self._ask_user(f"Are you sure you want to delete player {color_text(name,"yw")} and {color_text('all their characters ?',"rd")}"):
                        dict_changed = True
                        for entry in self.__player_dict:
                            if entry["owner"] != name:
                                new_player_dict.append(entry)
            else:
                if self.get_chars_of_player(name,False) == []:
                    print(color_text("Character not found.","yw"))
                else:
                    check_for_owner = self.get_chars_of_player(name)
                    if len(check_for_owner) <= 1:
                        if self._ask_user(f"Are you sure you want to delete {color_text(name,"yw")}"):
                            dict_changed = True
                            for entry in self.__player_dict:
                                if entry["name"] != name:
                                    new_player_dict.append(entry)
                    else:
                        print(f"Character {color_text(name,"yw")} is owner of another Character:")
                        self.print_chars(name,True)
        
            #if there are changes to the dict, save it           
            if dict_changed:
                self.__player_dict = new_player_dict
                self.save_player_dict()

    def get_chars_of_player(self,name:str,owner:bool=True) -> dict:
        search_key = ""
        if owner:
            search_key = "owner"
        else:
            search_key = "name"
        search_result = [entry for entry in self.__player_dict if entry[search_key].lower() == name.lower()]
        return search_result

    def print_chars(self,name:str="",owner:bool=False):
        print_this = {}
        if name != "":
            print_this = self.get_chars_of_player(name,owner)
        else:
            print_this = self.__player_dict

        #print main row
        main_row_keys = list(print_this[0].keys())
        main_row = f"|{color_text(" " + str(main_row_keys[0]) + " "*(self.__print_config['player'] - len(main_row_keys[0]) - 2),"blwb")}|"
        main_row += f"{color_text(" " + str(main_row_keys[1]) + " "*(self.__print_config['class'] - len(main_row_keys[1]) - 1),"blwb")}|"
        main_row += f"{color_text(" " + str(main_row_keys[2]) + " "*(self.__print_config['player'] - len(main_row_keys[2]) - 1),"blwb")}|"
        line_length = len(main_row) - 24
        print(main_row)
        print((line_length)*"-")

        #print characters
        for entry in print_this:
            char_row = f"| {str(entry["name"])}{(self.__print_config['player'] - len(entry["name"]) - 2)*" "}|"
            char_row += f" {str(entry["class"])}{(self.__print_config['class'] - len(entry["class"]) -1)*" "}|"
            char_row += f" {str(entry["owner"])}{(self.__print_config['player'] - len(entry["owner"]) -1)*" "}|"
            print(char_row)
            print((line_length)*"-")

    def search_player(self,name:str,show_msg:bool = True) -> list:
        if name == "":
            print("nothing to search")
        else:
            search_result = self.get_chars_of_player(name)
            if search_result != [] and show_msg:
                print(f"found player {name} as owner of:")
                self.print_chars(name)
            else:
                if show_msg:
                    print(color_text("player not found, searching for character","yw"))
                search_result = self.get_chars_of_player(name,False)
                if search_result != [] and show_msg:
                    print(f"found character {name} as alt of {search_result[0]["owner"]}")
                else:
                    if show_msg:
                        print(f"Player or Character {name} does not exist")
            return search_result
    
    def sort_players(self):
        dict_copy = self.__player_dict
        dict_copy = sorted(dict_copy, key=lambda item: item["name"])
        self.__player_dict = sorted(dict_copy, key=lambda item: item["owner"])