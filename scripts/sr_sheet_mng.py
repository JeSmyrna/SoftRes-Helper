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
        self.__col_len = [setting for setting in load_json("./Data/_config/config") if setting["name"] == "col_lengths"][0]
        self.__settings = dict
        self.__sr_sheet: list
        self.__player_dict: PlayerManager
        self.sr_sheet_name : str
    
    def start_sr_mng(self,player_dict:object):
        self.__player_dict = player_dict
        while True:
            print(chr(27) + "[2J") #clear terminal
            print_menu_title("SR Sheet Manager")
            self.get_menu(self.__directory)
            user_input = input("option: ")
            if user_input == "0":
                print("going back to main menu...")
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

            elif user_input == "3":
                print(f"loading {self.__directory[int(user_input)]}...")
                sleep(1)
                back_to = self.sr_sheet_mng(self.__directory[int(user_input)])
                if back_to == False:
                    print("going back to main menu...")
                    sleep(1)
                    return
        
            else:
                print("not an option...")
                sleep(1)

    def sr_sheet_mng(self,sr_sheet:str) -> bool:
        self.sr_sheet_name = sr_sheet
        self.__sr_sheet = load_csv(f"./Data/{sr_sheet}/{sr_sheet}")
        self.__settings = load_json(f"./Data/{sr_sheet}/settings")[0]
        
        while True:
            print(chr(27) + "[2J") #clear terminal
            print_loaded_file(sr_sheet)
            self.get_menu(self.__blueprint["sr_sheet_menu"])
            user_input = input("option: ")

            if user_input == "0":
                return False
            
            elif user_input == "1":
                return True
            
            elif user_input == "3":
                self.print_sr_sheet()
                input("press enter to continue...")

            elif user_input == "5":
                self.add_to_sheet()

            elif user_input == "6":
                if len(self.__sr_sheet) > 1:
                    self.print_sr_sheet()
                    sr_entry = input("\nCharacter to delete or (q)uit: ")
                    if sr_entry == "q":
                        pass
                    else:
                        self.log_sr_entry(sr_entry,"manually deleted")
                else:
                    input("no entries found...")
            
            elif user_input == "7":
                log_data = load_csv(f"./Data/{self.sr_sheet_name}/sr_awarded")
                self.get_menu(log_data)
                char_name = input("\nCharacter name: ")
                self.reinstantiate_log(char_name)
            else:
                print("not an option")
                sleep(1)

    def get_menu(self,menu:list=[]):
        for entry in menu:
            print(f"[{menu.index(entry)}] {entry}")
    
    def save_sr_directory(self):
        save_json("./Data/_config/sr_directory", [{"name":self.__directory}])

    def _save_sr_sheet(self):
        save_csv(f"./Data/{self.sr_sheet_name}/{self.sr_sheet_name}",self.__sr_sheet)

    def _look_for_entries(self,char_name:str,owner:bool = True) -> list:
        """
        Search the SR Sheet with Owner Name\n
        Get all entries in a list
        """
        search_for = 0
        if owner:
            search_for = 1

        search_result = [entry for entry in self.__sr_sheet if entry[search_for] == char_name]
        return search_result

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

    def print_sr_sheet(self):
        print(chr(27) + "[2J") #clear terminal
        header_row = ""
        for entry in self.__sr_sheet[0]:
            if entry == "player" or entry == "char":
                header_row += f"|{color_text(" " + entry + " " * (self.__col_len["player"] - len(entry)),"blwb")}"
            elif entry == "item":
                header_row += f"|{color_text(" " + entry + " " * (self.__col_len["item"] - len(entry)),"blwb")}"
            elif entry == "class":
                header_row += f"|{color_text(" " + entry + " " * (self.__col_len["class"] - len(entry)),"blwb")}"
            elif entry == "bonus":
                header_row += f"|{color_text(" " + entry + " " * (7 - len(entry)),"blwb")}"
            else:
                header_row += f"|{color_text(" " + entry + " " * (self.__col_len["col_len"] - len(entry)),"blwb")}"
        header_row += "|"
        print(header_row)
        print("-"*((len(header_row) - (8*len(self.__sr_sheet[0])))))

        if len(self.__sr_sheet) > 1:
            for entry in self.__sr_sheet[1:]:
                new_row = ""
                for value in entry:
                    if entry.index(value) == 0 or entry.index(value) == 1:
                        new_row += f"| {value}{' ' * (self.__col_len["player"] - len(value))}"
                    elif entry.index(value) == 2:
                        new_row += f"| {value}{' ' * (self.__col_len["class"] - len(value))}"
                    elif entry.index(value) == 3:
                        new_row += f"| {value}{' ' * (self.__col_len["item"] - len(value))}"
                    elif entry.index(value) == 4:
                        new_row += f"| {value}{' ' * (7 - len(str(value)))}"
                    else:
                        new_row += f"| {value}{' ' * (self.__col_len["col_len"] - len(value))}"
                new_row += "|"
                print(new_row)

    def _fill_days(self,present_last_day:bool = False) -> list:
        days_filled = ["-" for entry in self.__sr_sheet[0][5:]]
        if present_last_day:
            days_filled.pop(-1)
            days_filled.append("present")
        return days_filled

    def add_to_sheet(self,new_entry:list=[],auto:bool=False):
        """
        new_entry = [char_owner, char_name, class, item_name, bonus=0]
        """
        
        #manual add
        if auto != True:
            char_owner = ""
            presence_list = []
            self.__player_dict.print_chars()
            char_name = input("\nCharacter Name: ")
            sr_item = input("Sr Item Name: ")
            present = input(f"Present Last Raid day {self.__sr_sheet[0][-1]} ? (y/n): ")

            search_result = self.__player_dict.search_player(char_name,False)
            if search_result != []:
                char_owner = search_result[0]["owner"]
            
            if self._check_rules(char_name) == [True,True]:

                if present == "y":
                    presence_list = self._fill_days(True)
                else:
                    presence_list = self._fill_days()

                make_entry = [char_owner,char_name,search_result[0]["class"],sr_item,0]
                make_entry.extend(presence_list)
                self.__sr_sheet.append(make_entry)
                self._save_sr_sheet()
            else:
                print(f"Character has already the max amount of SR+/Characters in the current sheet")
                input("...")
                return
            
        else:
            new_entry.extend(self._fill_days())
            self.__sr_sheet.append(new_entry)
            self._save_sr_sheet()
            return

        input("...")

    def move_to_log(self,entry:dict):
        """
        Keys:\n
        name, class, item, bonus, comment, date_logged, data\n
        data example: 'yyyy-mm-dd:present,yyyy-mm-dd:absent'
        """
        # func to check the length of the loot log
        index = len(load_csv(f"./Data/{self.sr_sheet_name}/sr_awarded"))
        try:
            entry = [index,entry["name"],entry["class"],entry["item"],entry["bonus"],entry["comment"],entry["date_logged"],f'{entry["data"]}']
        except:
            print("wrong format, please read the doc")
        else:
            save_csv(f"./Data/{self.sr_sheet_name}/sr_awarded",entry,False)

    def log_sr_entry(self,character:str,log_msg:str):
        data = ""
        try:
            char_entry = [entry for entry in self.__sr_sheet if entry[1] == character]
        except:
            print("Error: log_sr_entry input not found")
            input("...")
            return
        else:
            if char_entry == []:
                print("character not found")
                input("...")
                return
            
            if len(char_entry) > 1:
                self.get_menu(char_entry)
                entry_num = input("option or (q)uit: ")
                if entry_num == "q":
                    return
                else:
                    try:
                        char_entry = char_entry[int(entry_num)]
                    except:
                        input("input error...")
                        return
            else:
                char_entry = char_entry[0]

            if input(f"Are you sure you want to move {character} with the SR+ on {char_entry[3]} with a bonus of {char_entry[4]} to the Logs? (y/n): ") == "y" and char_entry[0] != type(list):
                self.__sr_sheet.remove(char_entry)
                save_csv(f'./Data/{self.sr_sheet_name}/{self.sr_sheet_name}',self.__sr_sheet)
                for i in self.__sr_sheet[0][5:]:
                    data += f'{i}:{char_entry[self.__sr_sheet[0].index(i)]},'

                new_log = {"name":character,
                        "class":char_entry[2],
                        "item":f"{char_entry[3]}",
                        "bonus":char_entry[4],
                        "date_logged":get_date(),
                        "comment":log_msg,
                        "data":f'{data[:-1]}'}
                self.move_to_log(new_log)
                input("successfully moved to log...")
            else:
                print("cancel logging...")
                sleep(1)

    def _check_rules(self,char_name:str) -> list[bool]:
        check = []
        character_list = self.__player_dict.search_player(char_name,False)
        char_owner = character_list[0]["owner"]
        entry_amount = self._look_for_entries(char_owner)

        #check if multiple alt are allowed and if not if they player has already a character in
        if self.__settings['multichar'] == False and len(entry_amount) > 0: # type: ignore
            check.append(False)
        else:
            check.append(True)
         
        #check if the amount of SR+ meets the max amount of SR+ in settings
        if self.__settings['sr_amount'] > len([entry for entry in self.__sr_sheet if entry[1] == char_name]): # type: ignore
            check.append(True)
        else:
            check.append(False)

        return check

    def reinstantiate_log(self,char_name:str):
        character_list = self.__player_dict.search_player(char_name,False)
        try:
            char_owner = character_list[0]["owner"]
        except:
            print("reinstantiate input error")
            input("...")
        
        if self._check_rules(char_name) == [True,True]:
            header_row = self.__sr_sheet[0]
            data = load_csv(f"./Data/{self.sr_sheet_name}/sr_awarded")
            data = [entry for entry in data if entry[1] == char_name]

            if data == []:
                print("no character in log found")
                input("...")
                return
            
            if len(data) > 1:
                print(color_text(">> character has more than 1 entry in log, please choose...","yw"))
                self.get_menu(data)
                user_entry = input("Log Nr. or (q)uit: ")
                if user_entry == "q":
                    return
                try:
                    data = data[int(user_entry)]
                except IndexError:
                    print("IndexError: couldn't find log")
                    input("...")
                    return
            else:
                data = data[0]
            
            data_days = str(data[-1]).split(",")

            days = {}
            for entry in data_days:
                entry = entry.split(":")
                days.update({entry[0]:entry[1]})
            
            list_entry = [char_owner,data[1],data[2],data[3],data[4]]
            for entry in header_row[5:]:
                if entry in days.keys():
                    list_entry.append(days[entry])
                else:
                    list_entry.append("-")
            self.__sr_sheet.append(list_entry)
            self._save_sr_sheet()
            print("Succesfully instantiated the log into SR+ Sheet")
            input("...")
        else:
            print(f"Character has already the max amount of SR+/Characters in the current sheet") # type: ignore
            input("...")