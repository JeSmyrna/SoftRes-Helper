from file_import import load_json
from export import save_json

class PlayerManager():
    def __init__(self):
        self.__player_dict = []
        self.load_player_dict()

    def load_player_dict(self):
        self.__player_dict = load_json("./Data/_config/player_dict")

    def save_player_dict(self):
        save_json("./Data/_config/player_dict",self.__player_dict)

    def add_player(self,player:dict):
        """
        player = {'name','class','owner'}
        """
        if self.get_chars_of_player(player["name"],False) == []:
            self.__player_dict.append(player)
            self.save_player_dict()
        else:
            print("Character already exists")

    def delete_player(self,name:str="",del_all:bool=False):
        if name == "":
            print("nothing to delete")
        else:
            new_player_dict = []
            if del_all:
                if self.get_chars_of_player(name) == []:
                    print("Character owner not found.")
                else:
                    for entry in self.__player_dict:
                        if entry["owner"] != name:
                            new_player_dict.append(entry)
            else:
                if self.get_chars_of_player(name,False) == []:
                    print("Character not found.")
                else:
                    check_for_owner = self.get_chars_of_player(name)
                    if len(check_for_owner) == 1:
                        for entry in self.__player_dict:
                            if entry["name"] != name:
                                new_player_dict.append(entry)
                    else:
                        print(f"Character {name} is owner of another Character:")
                        self.print_all_chars(name)
        
            #if there are changes to the dict, save it           
            if new_player_dict != []:
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

    def print_all_chars(self,name:str=""):
        print_this = {}
        if name != "":
            print_this = self.get_chars_of_player(name)
        else:
            print_this = self.__player_dict

        for entry in print_this:
            print(entry)

    def search_player(self,name:str):
        if name == "":
            print("nothing to search")
        else:
            search_result = self.get_chars_of_player(name)
            if search_result != []:
                print(f"found player {name} as owner of:")
                self.print_all_chars(name)
            else:
                print("player not found, searching for character")
                search_result = self.get_chars_of_player(name,False)
                if search_result != []:
                    print(f"found character {name} as alt of {search_result[0]["owner"]}")
                else:
                    print(f"Player or Character {name} does not exist")