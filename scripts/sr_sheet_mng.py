from scripts.general_functions import get_date, color_text, print_loaded_file, print_menu_title
from scripts.file_import import load_json, load_csv
from scripts.export import save_json, save_csv
from scripts.player_mng import PlayerManager
from scripts.import_raidlogs import RaidLogImporter
from scripts.raidres_interact import RaidResActor
from scripts.gsheets import export_to_gsheet
import os, shutil
from time import sleep

debug = True

class SrSheetManager(RaidLogImporter):
    def __init__(self):
        self.__directory = load_json("./Data/_config/sr_directory")[0]["name"]
        self.__blueprint = [setting for setting in load_json("./Data/_config/config") if setting["name"] == "sr_sheet"][0]
        self.__col_len = [setting for setting in load_json("./Data/_config/config") if setting["name"] == "col_lengths"][0]
        self.__settings: dict
        self.__sr_sheet: list
        self.__player_dict: PlayerManager
        self.sr_sheet_name : str
        self.raidres_data : dict
        self.active_player : str
        self.raidres_actor = RaidResActor()
    
    def start_sr_mng(self,player_dict:object):
        self.__player_dict = player_dict
        while True:
            #print(chr(27) + "[2J") #clear terminal
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
            else:
                try:
                    print(f"loading {self.__directory[int(user_input)]}...")
                    sleep(1)
                    back_to = self.sr_sheet_mng(self.__directory[int(user_input)])
                    if back_to == False:
                        print("going back to main menu...")
                        sleep(1)
                        return
                except:
                    print("not an option...")
                    sleep(1)

    def format_num_to_int(self):
        for entry in self.__sr_sheet[1:]:
            entry[4] = int(entry[4])
            entry[5] = int(entry[5])

    def sr_sheet_mng(self,sr_sheet:str) -> bool:
        self.sr_sheet_name = sr_sheet
        self.__sr_sheet = load_csv(f"./Data/{sr_sheet}/{sr_sheet}")
        self.format_num_to_int()
        self.__settings = load_json(f"./Data/{sr_sheet}/settings")
        
        while True:
            #print(chr(27) + "[2J") #clear terminal
            print_loaded_file(sr_sheet)
            self.get_menu(self.__blueprint["sr_sheet_menu"])
            user_input = input("option: ")

            if user_input == "0":
                return False
            
            elif user_input == "1":
                return True
            
            elif user_input == "2":
                self.get_menu(["go back\n","Sheet Settings","Print Settings"])
                try:
                    setting_option = int(input("option: "))-1
                    if setting_option < 0 or setting_option > 2:
                        pass
                    else:
                        self.settings_menu(setting_option)
                except:
                    pass

            elif user_input == "3":
                self.calc_bonus_roll()
                self.sort_sr_sheet([[1,False]])
                self._save_sr_sheet()
                self.print_sr_sheet()
                input("press enter to continue...")
            
            elif user_input == "4":
                self.make_new_entry()
                input("...") #delete later

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

            elif user_input == "8":
                self.sort_sr_sheet([[5,True],[3,False]])
                self.print_sr_sheet()
                export_to_gsheet(self.__sr_sheet)

            elif user_input == "9":
                self.raidres_actor.set_sr_sheet(self.__sr_sheet)

                raidres_link = input("RaidRes Link: ")

                self.raidres_actor.scan_site(raidres_link)
                input("...")
            elif user_input == "99":
                self.import_old_data()
            else:
                print("not an option")
                sleep(1)

    def get_menu(self,menu:list=[],break_line:bool = False,line_len:int=10,line_pos:list=[]):
        menu_copy = menu.copy()
        if break_line and len(line_pos) > 0:
            for pos in line_pos:
                menu_copy.insert(pos,'-'*line_len)
        list_index = 0
        for entry in menu_copy:
            try:
                if entry[0] == '-':
                    print(entry)
                else:
                    print(f"[{list_index}] {entry}")
                    list_index += 1
            except:
                pass
    
    def settings_menu(self,setting:int):
        options = ["go back\n"]
        settings = [entry for entry in self.__settings[setting]]
        options.extend(settings)

        while True:
            print(chr(27) + "[2J") #clear terminal
            self.show_settings(self.__settings[setting])
            self.get_menu(options)
            user_input = input("\noption: ")
            if user_input == "0":
                return
            try:
                if int(user_input) <= 0:
                    print("Can't be negative or 0")
                    input("...")
                else:
                    self.change_setting(self.__settings[setting][options[int(user_input)]],setting_name=options[int(user_input)],setting_num=setting)
            except IndexError:
                print("settings_menu: INDEX error")
            except:
                print("settins_menu: Input error")
            save_json(f"./Data/{self.sr_sheet_name}/settings",self.__settings)

    def show_settings(self,settings):
        header = [entry for entry in settings]
        values = [settings[entry] for entry in settings]
        line_len = len(header) * self.__col_len['player'] + len(header) + 1
        header_row = "|"
        for entry in header:
            header_row += color_text(f" {entry}{" " * (self.__col_len["player"] - len(entry) - 1)}","blwb")
            header_row += "|"
        print(header_row)
        print("-" * line_len)

        value_row = "|"
        for entry in values:
            value_row += f" {entry}{" " * (self.__col_len["player"] - len(str(entry)) - 1)}"
            value_row += "|"
        print(value_row)
        print("-" * line_len + "\n")
        
    def change_setting(self,setting,setting_name,setting_num:int):
        while True:
            if type(setting) == bool:
                self.__settings[setting_num][setting_name] = not self.__settings[setting_num][setting_name]
                break
            else:
                user_input = input(f"New value for {setting_name}: {setting} >> ")
                try:
                    self.__settings[setting_num][setting_name] = int(user_input)
                    break
                except:
                    print("change setting: input error")

    def change_entry(self):
        sr_entry_menu = ["go back\n"]
        sr_entry_menu.extend([entry for entry in self.__sr_sheet[1:]])
        while True:
            print(chr(27) + "[2J") #clear terminal
            self.get_menu(sr_entry_menu)
            try:
                entry_to_edit = int(input("Entry Num: "))
            except:
                pass
            else:
                if entry_to_edit == 0:
                    break
                else:
                    while True:
                        for value in self.__sr_sheet[entry_to_edit][6:]:
                            print(value)

                        input("...")

    def save_sr_directory(self):
        save_json("./Data/_config/sr_directory", [{"name":self.__directory}])

    def _save_sr_sheet(self,copy:bool = False):
        """
        copy = True, copies sr_sheet into the log folder\n
        with the last entry in the header column from sheet
        """
        file_path = f"./Data/{self.sr_sheet_name}/{self.sr_sheet_name}"
        if copy:
            target_path = f"./Data/{self.sr_sheet_name}/sr_saves/sr_sheets/{self.__sr_sheet[0][-1]}-{self.sr_sheet_name}.csv"
            if os.path.exists(target_path):
                pass
            else:
                shutil.copy(f"{file_path}.csv",target_path)
        else:
            save_csv(file_path,self.__sr_sheet)

    def _look_for_entries(self,char_name:str,owner:bool = True) -> list:
        """
        Search the SR Sheet with Owner Name\n
        Get all entries in a list
        """
        search_for = 1
        if owner:
            search_for = 0

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

            save_json(f"{new_path}settings",[self.__blueprint["settings"],self.__blueprint["print_settings"]])
            save_csv(f"{new_path}{raidname}",[self.__blueprint["columns"]])
            save_csv(f"{new_path}sr_awarded",[self.__blueprint["awarded"]])

    def print_sr_sheet(self,specific_entry:str=""):
        print(chr(27) + "[2J") if debug == False else 0 #clear terminal
        header_row = ""
        columns = self.__sr_sheet[0].copy()
        #indecies to print
        indecies_to_print = []
        option_keys = list(self.__settings[1].keys())
        for key in option_keys:
            if self.__settings[1][key] == True:
                indecies_to_print.append(option_keys.index(key))
        if len(columns) > 13:
            for entry in columns[-6:]:
                indecies_to_print.append(columns.index(entry))
        else:
            for entry in columns[7:]:
                indecies_to_print.append(columns.index(entry))

        for entry in indecies_to_print:
            if columns[entry] == "player" or columns[entry] == "char":
                header_row += f"|{color_text(" " + columns[entry] + " " * (self.__col_len["player"] - len(columns[entry])),"blwb")}"
            elif columns[entry] == "item":
                header_row += f"|{color_text(" " + columns[entry] + " " * (self.__col_len["item"] - len(columns[entry])),"blwb")}"
            elif columns[entry] == "class":
                header_row += f"|{color_text(" " + columns[entry] + " " * (self.__col_len["class"] - len(columns[entry])),"blwb")}"
            elif "bonus" in columns[entry]:
                header_row += f"|{color_text(" " + columns[entry] + " " * (7 - len(columns[entry])),"blwb")}"
            else:
                header_row += f"|{color_text(" " + columns[entry] + " " * (self.__col_len["col_len"] - len(columns[entry])),"blwb")}"
            
        header_row += "|"
        print(header_row)
        print("-"*((len(header_row) - (8*len(indecies_to_print)))))

        entries_to_print:list
        if specific_entry != "":
            entries_to_print = [entry for entry in self.__sr_sheet if entry[0] == specific_entry]
        else:
            entries_to_print = self.__sr_sheet[1:]

        if len(self.__sr_sheet) > 1:
            divider_line = 0
            for entry in entries_to_print:
                new_row = ""
                for i in indecies_to_print:
                    try:
                        value = entry[i]
                        if i == 0 or i == 1:
                            new_row += f"| {value}{' ' * (self.__col_len["player"] - len(value))}"
                        elif i == 2:
                            new_row += f"| {value}{' ' * (self.__col_len["class"] - len(value))}"
                        elif i == 3:
                            new_row += f"| {value}{' ' * (self.__col_len["item"] - len(value))}"
                        elif i == 5 or i == 4:
                            new_row += f"| {value}{' ' * (7 - len(str(value)))}"
                        else:
                            day = value
                            if day == 'present':
                                day = color_text(day,'gr')
                            elif day == 'absent':
                                day = color_text(day,'rd')
                            new_row += f"| {day}{' ' * (self.__col_len["col_len"] - len(value))}"
                    except:
                        print("Uneven length between header row and entries, reload SR Sheet")
                        return
                new_row += "|"
                print(new_row)
                divider_line += 1
                if divider_line % 5 == 0:
                    print("-"*((len(header_row) - (8*len(indecies_to_print)))))
            if divider_line % 5 != 0:
                print("-"*((len(header_row) - (8*len(indecies_to_print)))))

    def _fill_days(self,present_last_day:bool = False) -> list:
        days_filled = ["-" for entry in self.__sr_sheet[0][7:]]
        if present_last_day:
            days_filled.pop(-1)
            days_filled.append("present")
        return days_filled

    def add_to_sheet(self,new_entry:list=[],auto:bool=False):
        """
        new_entry = [char_owner, char_name, class, item_name, prev_bonus=0, bonus=0, status]
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

                make_entry = [char_owner,char_name,search_result[0]["class"],sr_item,0,0,"active"]
                make_entry.extend(presence_list)
                self.__sr_sheet.append(make_entry)
                self._save_sr_sheet()
            else:
                print(f"Character has already the max amount of SR+/Characters in the current sheet")
                input("...")
                return
            
        else:
            new_entry.extend(self._fill_days())#delete that raider here last raid = True
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
        log_data = load_csv(f"./Data/{self.sr_sheet_name}/sr_awarded")
        index = len(log_data)
        if len(log_data[1:]) > 100:
            first_entry = log_data[1][6]
            last_entry = log_data[-1][6]
            log_copy_path = f"./Data/{self.sr_sheet_name}/sr_saves/sr_awarded/{first_entry}-{last_entry}_SR_awarded.csv"
            shutil.copy(f"./data/{self.sr_sheet_name}/sr_awarded.csv",log_copy_path)
            save_csv(f"./Data/{self.sr_sheet_name}/sr_awarded",self.__blueprint["awarded"],True)
        try:
            entry = [index,entry["name"],entry["class"],entry["item"],entry["bonus"],entry["comment"],entry["date_logged"],f'{entry["data"]}']
        except:
            print("wrong format, please read the doc")
        else:
            save_csv(f"./Data/{self.sr_sheet_name}/sr_awarded",entry,False)

    def _format_log(self,entry:list,log_msg:str="") -> dict:
        """
        formats sr entries into log entries > return dictionary for move_to_log
        """
        data = ""
        for i in self.__sr_sheet[0][7:]:
            data += f'{i}:{entry[self.__sr_sheet[0].index(i)]},'
        new_log = {"name":entry[1],
                "class":entry[2],
                "item":f"{entry[3]}",
                "bonus":entry[4],
                "date_logged":get_date(),
                "comment":log_msg,
                "data":f'{data[:-1]}'}
        return new_log

    def log_sr_entry(self,character:str="",log_msg:str="",auto:bool=False,entry:list=[]):
        if auto:
            self._format_log(entry,log_msg)
            self.__sr_sheet.remove(entry)
            self._save_sr_sheet()

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
                new_log = self._format_log(char_entry,log_msg)
                
                self.move_to_log(new_log)
                self.__sr_sheet.remove(char_entry)
                self._save_sr_sheet()
                input("successfully moved to log...")
            else:
                print("cancel logging...")
                sleep(1)

    def _check_rules(self,char_name:str) -> list[bool]:
        """
        gives back a list of True/False, depending on checked rules\n
        [0] multichar - if alt characters are allowed\n
        [1] sr_amount - if character is allowed an additional SR+
        """
        check = []
        character_list = self.__player_dict.search_player(char_name,False)
        print(f"Found Characters: {character_list}") if debug == True else 0
        char_owner = character_list[0]["owner"]
        print(f"Found Character Owner: {char_owner}") if debug == True else 0
        entry_amount = self._look_for_entries(char_owner)
        print(f"Found SR in sheet: {entry_amount}") if debug == True else 0
        #check if multiple alt are allowed and if not if they player has already a character in
        if self.__settings[0]['multichar'] == False and len(entry_amount) > 0: # type: ignore
            print(f"No Alts allowed, at least 1 Alt has a SR: {self.__player_dict.get_chars_of_player(char_owner)}") if debug == True else 0
            check.append(False)
        else:
            print(f"Alts are allowed or no other Alt yet in Sheet, Keep going") if debug == True else 0
            check.append(True)
         
        #check if the amount of SR+ meets the max amount of SR+ in settings
        if self.__settings[0]['sr_amount'] > len([entry for entry in self.__sr_sheet if entry[1] == char_name]): # type: ignore
            print(f"{char_name} has room for another SR") if debug == True else 0
            check.append(True)
        else:
            print(f"{char_name} has max SR entries") if debug == True else 0
            check.append(False)

        return check

    def reinstantiate_log(self,char_name:str):
        character_list = self.__player_dict.search_player(char_name,False)
        try:
            char_owner = character_list[0]["owner"]
        except:
            print("reinstantiate input error")
            input("...")
            return
        
        if self._check_rules(char_name) == [True,True]:
            header_row = self.__sr_sheet[0]
            data_import = load_csv(f"./Data/{self.sr_sheet_name}/sr_awarded")
            data = [entry for entry in data_import if entry != []]
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
            
            list_entry = [char_owner,data[1],data[2],data[3],0,data[4],"active"]
            for entry in header_row[7:]:
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

    def sort_sr_sheet(self,sort_by:list):
        """
        Input: A List with Lists containing [int,bool]\n
        Int = column names ID: 0 - owner, 1 - char, 2 - class, 3 - item , 4 - prev_bonus, 5 - bonus\n
        Bool = sort reverse or not
        """
        sorted_list = self.__sr_sheet.copy()
        for sorting in sort_by:
            sorted_list = sorted(sorted_list[1:], key=lambda x:x[sorting[0]], reverse=sorting[1])

        sorted_list.insert(0, self.__sr_sheet[0])
        self.__sr_sheet = sorted_list

    def choose_sr_of_player(self):
        """
        adds new SR+ for player to sheet\n
        Needs self.active_player
        """
        #players at this point should be in the player dicitionary
        player_data = self.__player_dict.search_player(self.active_player,False)[0]
        player_sr_plus = [entry[3] for entry in self.__sr_sheet if entry[1] == self.active_player]
        header_line = f"|{color_text(' '*23 + 'item'+' '*24,'blwb')}|{color_text(' '*21+'comment'+' '*21,'blwb')}|"
        
        player_sr = self.raidres_data.get(self.active_player)
        if player_sr == None:
            print(f"player {self.active_player} not found in raidres")
            return
        comment_start = len(player_sr)//2 #dynamic index
        res_menu = [f"Nothing{" "*41}| {" "*48}|"]
        for entry in player_sr[0:comment_start]:
            item_comment = player_sr[comment_start+player_sr.index(entry)]
            res_menu.append(f"{entry}{" "*(self.__col_len['item'] - len(entry))}| {item_comment}{" "*(self.__col_len['item'] -len(item_comment))}|")
        
        while True:
            print(header_line)
            print("-"*(self.__col_len['item'] * 2 + 7))
            self.get_menu(res_menu,break_line=True,line_len=103,line_pos=[1])
            print("-"*(self.__col_len['item'] * 2 + 7))
            try:
                user_input = int(input(f"new SR+ for {color_text(self.active_player,'yw')}: "))
            except:
                print(f"input {user_input} is not a number")
            #print(f"input = {user_input} | type: {type(user_input)}")
            if user_input == 'q':
                input("Jumping to next attendee...")
                return
            try:
                if user_input == 0:
                    print(f'Adding {self.active_player} with Nothing')
                    self.add_to_sheet([player_data['owner'],player_data['name'],player_data['class'],'Nothing',0,0,'active'],True)
                else:
                    #prevent double sr+
                    if player_sr[user_input-1] not in player_sr_plus:
                        print(color_text(f'{self.active_player}','yw')+f' new SR+: {player_sr[user_input-1]}')
                        self.add_to_sheet([player_data['owner'],player_data['name'],player_data['class'],player_sr[user_input-1],0,0,'active'],True)
                    else:
                        input("Can't put in the same SR...")
                print("-"*(self.__col_len['item'] * 2 + 7)+'\n')
                sleep(1)
                if self._check_rules(self.active_player) == [False,True]:
                    #delete item from list to prevent doublicates
                    if user_input != 0:
                        print(f"deleting: {res_menu[user_input]}")
                        res_menu.pop(int(user_input))
                    else:
                        pass
                else:
                    return
            except:
                input("Item not found, try again...\n")

    def doc_attendance(self,attendance:list):
        """
        Documents attendance of each player in SR+ Sheet\n
        Either present, absent or half run
        """
        while True:
            clear_status = input("Full Clear ? (y/n): ")
            if clear_status in "yn":
                break
            else:
                print('Input wrong. Try again.')

        for entry in self.__sr_sheet[1:]:
            if entry[1] in attendance:
                if clear_status == 'y':
                    entry.append('present')
                elif clear_status == 'n':
                    entry.append('half run')
            else:
                entry.append('absent')

    def calc_bonus_roll(self):
        """
        Only Calculates bonusroll for all entries in the SR Sheet
        """
        for entry in self.__sr_sheet[1:]:
            decay_counter = 0
            bonus_roll = 0
            if entry[3].lower() == "nothing":
                pass
            else:
                for day in entry[7:]:
                    if day == 'present':
                        bonus_roll += self.__settings[0]['bonus']
                    elif day == 'half run':
                        bonus_roll += self.__settings[0]['bonus_half']
                    elif day == 'absent':
                        if self.__settings[0]['decay'] == True:
                            decay_counter += 1
                            if decay_counter == self.settings_menu[0]['decay_after']:
                                bonus_roll -= self.__settings[0]['decay_amount']
                                decay_counter = 0
                    else:
                        pass
            entry[5] = bonus_roll + int(entry[4])

    def check_absent_days(self):
        """
        Check abescence of all players in the SR Sheet.\n
        Auto deletion of players that have an absence of self.settings[del_p_after]
        """
        for entry in self.__sr_sheet[1:]:
            #prevent frozen players being deleted
            if entry[6] == "active" and entry[3].lower() != "nothing":
                absent_days = 0
                for day in entry[7:]:
                    if day == 'absent':
                        absent_days += 1
                    elif day == 'present' or day == 'half run':
                        absent_days = 0
                #after checking should only delete player if the last played raids are higher than set
                if absent_days >= self.__settings[0]['del_p_after']:
                    #self.log_sr_entry(entry[1],f"Player was absent for {absent_days} raids. Auto Deleted",True,entry)
                    self.move_to_log(self._format_log(entry,f"Player was absent for {absent_days} raids. Auto Deleted"))
            else:
                pass
    
    def show_raidres_overview(self,data:list):
        """
        Get an Overview of all attendees soft reserves and SR pluss in sheet
        """
        raidres = data[3]
        line_len = self.__col_len['player'] + self.__col_len['item'] + self.__col_len['item'] + 5
        print('='*line_len)
        for entry in raidres:
            if entry in data[1]:
                player_sr = raidres[entry]
                comment_start = len(player_sr)//2 #dynamic index

                #first print all raid res entries
                player_name = entry
                for sr_entry in player_sr[0:comment_start]:
                    raidres_text = ""
                    item_comment = player_sr[comment_start+player_sr.index(sr_entry)]
                    raidres_text += f"{player_name}{' '*(self.__col_len['player'] - len(player_name))}|"
                    raidres_text += f" {sr_entry}{' '*(self.__col_len['item'] - len(sr_entry))}|"
                    raidres_text += f" {item_comment}{' '*(self.__col_len['item'] - len(item_comment))}|"
                    print(raidres_text)
                    player_name = ""

                sr_entries = [sr_plus for sr_plus in self.__sr_sheet if sr_plus[1] == entry]
                print('-'*line_len)

                #Then print all entries in SR Sheet
                for sr in sr_entries:
                    row_text = ""
                    row_text = f'{sr[1]}{' '*(self.__col_len['player'] - len(sr[1]))}|'
                    row_text += f' {color_text(sr[3],'yw')}{" "* (self.__col_len["item"] - len(sr[3]))}|'
                    row_text += f' Bonusroll: {sr[5]}{" "* (self.__col_len['item'] - int(sr[5]) -12)}|'
                    print(row_text)

                print('='*line_len)

    def award_through_lootlog(self,data:list):
        loot_list = [entry.split(": ") for entry in data]
        #format loot log to dictionary
        loot_dict = {}
        for entry in loot_list:
            if entry[-1] in loot_dict.keys():
                entry_value = loot_dict[entry[-1]]
                if len(entry) > 2:
                    new_entry = ": ".join(list(entry[:len(entry)-1]))
                    entry_value.append(new_entry)
                else:
                    entry_value.append(entry[0])
                loot_dict.update({entry[-1]:entry_value})
            else:
                loot_dict.update({entry[-1]:[entry[0]]})
        
        keys = list(loot_dict.keys())
        keys.sort()
        sr_plus_winners = []

        for key in keys:
            search_result = [entry for entry in self.__sr_sheet[1:] if entry[1] == key and entry[3] in loot_dict[key]]
            if search_result != []:
                for log in search_result:
                    if input(f"{log[1]} won {log[3]} on the {self.__sr_sheet[0][-1]} with a Bonusroll of {log[5]} (y/n): ") == 'y':
                        self.move_to_log(self._format_log(log,f"Won SR+ on {self.__sr_sheet[0][-1]}"))
                        self.__sr_sheet.remove(log)
                        sr_plus_winners.append(log[1])
        print("Awarding through Loot Log done")
        win_text = ""
        for winner in sr_plus_winners:
            win_text += f" {winner},"
        print(f"Congratulations to:{win_text[0:-2]} for winning their SR Plus.\n")

    def make_new_entry(self):
        imported_data = self.import_logs()
        self.raidres_data = imported_data[3]

        if imported_data == None:
            input("...")
            return
        
        #make safety copy
        if len(self.__sr_sheet) > 1:
            self._save_sr_sheet(True)
        
        #Check attendee if already registered
        for attendee in imported_data[1]:
            #Add players not found
            #Look if player is in player dictionary
            if self.__player_dict.search_player(attendee,False) == []:
                #func for adding player
                self.add_player_to_dict(attendee,imported_data[3])
                    
        
        #get all char names in sr sheet
        print(f"Getting all Characters in Sheet") if debug == True else 0
        characters_in_sheet = [char[1] for char in self.__sr_sheet]
        attendee_copy = imported_data[1].copy()

        for attendee in imported_data[1]:
            print(" "* 50) if debug == True else 0
            print(f"Check for: {color_text(attendee,'yw')}") if debug == True else 0
            self.active_player = attendee
            #Check if attendee is NOT in SR sheet
            if attendee not in characters_in_sheet:
                print(f"Character not in sheet") if debug == True else 0
                #check if alt of any owner and alts allowed
                if self._check_rules(self.active_player)[0] == True:
                    print(f"Check rules done: continue to choose SR for player {attendee}") if debug == True else 0
                    self.choose_sr_of_player()
                #if not check present for owner
                else:
                    owner = self.__player_dict.get_chars_of_player(self.active_player,False)[0]['owner']
                    raidres_of_player = imported_data[3].get(self.active_player)
                    if raidres_of_player == None:
                        raidres_of_player = []
                    self.show_entries(raidres_of_player)
                    self.print_sr_sheet(specific_entry=owner)
                    active_entry = [entry for entry in self.__sr_sheet if entry[0] == owner][0]
                    if input(f"\nDo you want to replace the SR of {active_entry[1]} with SR of {attendee} (y/n)") == 'y':
                        sr_in_sheet = [entry for entry in self.__sr_sheet if entry[0] == owner]
                        self.move_to_log(self._format_log(sr_in_sheet[0],f"Replacing SR with Alt {attendee}"))
                        self.choose_sr_of_player()
            
            #attendee is in sr sheet
            else:
                print(f"Attendee is in sr sheet, getting all raidres entries...") if debug == True else 0
                player_sr = self.raidres_data.get(self.active_player)
                print(f"Looking for RaidRes Entries: {player_sr}") if debug == True else 0
                if player_sr == None:
                    print(f"found None for {attendee}, replacing with an empty List") if debug == True else 0
                    player_sr = []
                print(f"Looking for SR Entries in SR Sheet...") if debug == True else 0
                player_sr_plus = [entry for entry in self.__sr_sheet[1:] if entry[1] == self.active_player]
                print(f"Found {len(player_sr_plus)}: {player_sr_plus}") if debug == True else 0
                #check if attendees soft reserve are the same as in the sheet
                print(f"Checking found Entries if in Raidres...") if debug == True else 0
                for entry in player_sr_plus:
                    
                    if entry[3] in player_sr:
                        print(f"{entry} found in Sheet") if debug == True else 0
                        #found the SR+
                        pass
                    else:
                        print(f"Couldn't find {entry} in SR Sheet") if debug == True else 0
                        #printing raidres and comment
                        self.show_entries(player_sr)

                        #didn't find the SR+ > Delete?
                        print(f"{self.active_player} has not reserved the same item: {entry[3]} Bonusroll: {entry[5]}")
                        if input("y/n: ") == "y":
                            if entry[3].lower() != "nothing":
                                self.move_to_log(self._format_log(entry,"Player didn't reserve same item"))
                            self.__sr_sheet.remove(entry)
                            self._save_sr_sheet()
                            self.choose_sr_of_player()

                #check if attendee has the same amount of SR+ as sheet allows
                if self._check_rules(self.active_player)[1] == True:
                    print(f"{attendee} has room for {self.__settings[0]['sr_amount'] - len(player_sr_plus)} SR Plus") if debug == True else 0
                    self.choose_sr_of_player()

        #Check comments on players soft reserves
        while True:
            print(chr(27) + "[2J") if debug != True else 0 #clear terminal
            self.show_raidres_overview(imported_data)
            self.get_menu(['continue\n','type character name to change entry'])
            user_input = input("option or name: ")
            if user_input == '0':
                break
            else:
                print(f"Changing entry for {user_input.capitalize()}") if debug == True else 0
                #doesnt find alts of char yet, ADD SOON
                sr_entries = [entry for entry in self.__sr_sheet if entry[1] == user_input.capitalize()]
                print(f"Found SR Entries: {sr_entries}") if debug == True else 0
                if sr_entries != []:
                    self.active_player = user_input
                    while True:
                        menu_items = [[item[3],f"Bonusroll: {item[5]}"] for item in sr_entries]
                        sr_entries_menu = []
                        item_names = []
                        bonus_rolls = []
                        for opt in menu_items:
                            item_names.append(opt[0])
                            bonus_rolls.append(opt[1])
                        sr_entries_menu.extend(item_names)
                        sr_entries_menu.extend(bonus_rolls)
                        print(sr_entries_menu) if debug == True else 0
                        self.show_entries(sr_entries_menu)
                        try:
                            user_input = int(input("option: "))
                            if user_input == 0:
                                break
                            user_input -= 1
                        except:
                            print("input must be a number in range.\n")
                        else:
                            print(f"moving {sr_entries[user_input]} to log")  if debug == True else 0
                            self.move_to_log(self._format_log(sr_entries[user_input],"Changed to a different SR+"))
                            print("removing from sr sheet") if debug == True else 0
                            self.__sr_sheet.remove(sr_entries[user_input])
                            print("choose new SR...") if debug == True else 0
                            self.choose_sr_of_player()
                            self._save_sr_sheet()
                            break
                else:
                    input("Couldn't find character...")
        
        #New column name for SR Sheet
        new_entry_name = input("New Date (YYYY-MM-DD): ")
        self.__sr_sheet[0].append(new_entry_name)
        self.doc_attendance(attendee_copy)

        #Auto Delete players after certain days, if setting is active
        if self.__settings[0]['del_player'] == True:
            self.check_absent_days()

        #Check loot log and move to log file if won
        self.award_through_lootlog(imported_data[2])

        self.calc_bonus_roll()
        self._save_sr_sheet()
        #Log the raid logs func
        self.safe_imported_logs(self.sr_sheet_name,self.__sr_sheet[0][-1],imported_data[0])
        
    def add_player_to_dict(self,attendee:str,raidres_data:dict={}):
        new_player_entry = {'name':attendee}
        if self.__player_dict._ask_user(f"-----\nAdd {attendee} as alt?"):
            while True:
                ask_owner_name = input("owner:")
                search_result = self.__player_dict.get_chars_of_player(ask_owner_name)
                if search_result != []:
                    if self.__player_dict._ask_user(f"Do you want to add {ask_owner_name} as owner of {attendee}?"):
                        new_player_entry.update({'owner':ask_owner_name})
                        break
                else:
                    input(f"Couldn't find player {ask_owner_name}...")
                    if self.__player_dict._ask_user("Rather add character also as owner?"):
                        new_player_entry.update({'owner':attendee})
                        break
        else:
            new_player_entry.update({'owner':attendee})

        newPlayerData = raidres_data.get(attendee)
        if newPlayerData != None:
            new_player_entry.update({'class':newPlayerData[-1]})
        else:
            print(f"player {color_text(attendee,"yw")} not found in raidres, not enough information to add to player dict\n-----")
            new_player_entry.update({'class':self.__player_dict.choose_class()})
        self.__player_dict.add_player(new_player_entry)

    def show_entries(self,player_sr):
        comment_start = len(player_sr)//2 #dynamic index
        res_menu = [f"Nothing{" "*41}| {" "*48}|"]
        for entry in player_sr[0:comment_start]:
            item_comment = player_sr[comment_start+player_sr.index(entry)]
            res_menu.append(f"{entry}{" "*(self.__col_len['item'] - len(entry))}| {item_comment}{" "*(self.__col_len['item'] -len(item_comment))}|")
        header_line = f"|{color_text(' '*23 + 'item'+' '*24,'blwb')}|{color_text(' '*21+'comment'+' '*21,'blwb')}|"
        print(header_line)
        print("-"*(self.__col_len['item'] * 2 + 7))
        self.get_menu(res_menu,break_line=True,line_len=103,line_pos=[1])
        print("-"*(self.__col_len['item'] * 2 + 7))

    def import_old_data(self):
        path = input("csv filepath: ")
        imported_data = load_csv(path.strip(".csv"))
        self._save_sr_sheet(True)
        #check if character are in player dictionary
        column_names = [day for day in imported_data[0][4:]]
        self.__sr_sheet[0].extend(column_names)
        for entry in imported_data[1:]:
            search_result = self.__player_dict.search_player(entry[0],False)
            #Doesn't exist yet
            if search_result == []:
                self.add_player_to_dict(entry[0])
            else:
                pass
            #look for entries of that character
            if self._look_for_entries(entry[0]) == []:
                if self._check_rules(entry[0]) == [True,True]:
                    found_char = self.__player_dict.get_chars_of_player(entry[0],False)
                    owner_name = found_char[0]['owner']
                    char_class = found_char[0]['class']
                    new_entry = [owner_name,entry[0],char_class,entry[1],int(entry[2]),0,"active"]
                    new_entry_days = [day for day in entry[4:]]
                    new_entry.extend(new_entry_days)
                    self.__sr_sheet.append(new_entry)
        input("Import done...")