import os,shutil

from scripts.file_import import load_text_file, load_csv

class RaidLogImporter():
    def __init__(self):
        pass

    def print_list(self,file_list:list,show_identifier:bool=False):
        counter = 0
        longest_file_name = max([len(file) for file in file_list])+10
        identifier = ['raider name list','loot Log','raidres exported csv']
        print("Files".center(50,"="))
        for file in file_list:
            counter += 1
            part_a = f'[{counter}] - {file}'
            if show_identifier:
                print(f'{part_a}{(longest_file_name - len(part_a)) * ' '}- {identifier[counter - 1]}')
            else:
                print(part_a)
        print("="*50)

    def sort_files_attendance_loot_raidres(self,files:list) -> list:
        for file in files:
            if file[-3:] == 'csv':
                raidres_file = file
            elif "loot" in file.lower():
                loot_file = file
            else:
                attendance_file = file
        try:
            sorted_list = [attendance_file,loot_file,raidres_file]
            print('-'*50)
            print("Auto identified files")
        except:
            print("Could not auto identify files")
            return []
        return sorted_list

    def manually_choose_files(self,input_list:list) -> list:
        sorted_list = []
        print('-'*20)
        print("Which is the loot file?")
        self.print_list(input_list)
        try:
            user_input = int(input("File: "))
            sorted_list.append(input_list[user_input - 1])
            input_list.pop(user_input - 1)
        except IndexError:
            print("import_raidlogs.py: input is out of range")
        except:
            print("import_raidlogs.py: input must be a number")
        
        for file in input_list:
            if file[-3:] == 'csv':
                sorted_list.append(file)
            else:
                sorted_list.insert(0,file)
        return sorted_list

    def import_logs(self) -> tuple[list,list,list,dict]:
        """
        gets files from Import folder. Make sure its 3.\n
        return: sorted list, attendeese, loot log, raidres
        """
        import_list = os.listdir("./Import/")
        if import_list == []:
            print("Import folder is empty")
            return
        elif len(import_list) < 3:
            print("Missing files in Import folder.\n3 Files needed. loot.txt, raider.txt and raidres.csv")
            return
        
        sorted_list = self.sort_files_attendance_loot_raidres(import_list)
        while True:
            if sorted_list != []:
                self.print_list(sorted_list,True)
                user_input = input("Is this correct ? (y/n): ")
                if user_input == 'y':
                    break
                elif user_input == 'n':
                    sorted_list = self.manually_choose_files(sorted_list)
                else:
                    print("invalid input")
                    print('-'*20)
            else:
                sorted_list = self.manually_choose_files(import_list)
        
        attendeese = load_text_file(f'./Import/{sorted_list[0][:-4]}')
        loot_log = load_text_file(f'./Import/{sorted_list[1][:-4]}',20)
        raidres = self.get_players_sr_and_comments(f'{sorted_list[2][:-4]}')
        
        attendeese.sort()

        return sorted_list,attendeese,loot_log,raidres

    def get_players_sr_and_comments(self,filename="raidres"):
        raidres_list = load_csv(f'Import/{filename}')
        raid_res_player_dict = {}

        #make key list
        keys = [attendee[1] for attendee in raidres_list if attendee[1] != 'Attendee']
        keys.sort()
        for key in keys:
            items = []
            comments = []
            char_class = ""
            for item in raidres_list:
                if key == item[1]:
                    items.append(item[0])
                    comments.append(item[3])
                    char_class = item[2].capitalize()
            """ if len(items) == 1:
                items.append(items[0])
                comments.append('') """
            items.extend(comments)
            items.append(char_class)
            raid_res_player_dict.update({key:items})
        return raid_res_player_dict

    def safe_imported_logs(self,filename:str,date:str,logs:list):

        filepath = f'./Data/{filename}/logs/'

        shutil.move(f"./Import/{logs[0]}",f'{filepath}/{date}_raider.txt')
        shutil.move(f"./Import/{logs[1]}",f'{filepath}/{date}_loot.txt')
        shutil.move(f'./Import/{logs[2]}',f'{filepath}/{date}_{logs[2][-10:]}')
        
        print(f"saved logs in: {filepath}")
    
    