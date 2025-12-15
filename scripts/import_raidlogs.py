import os,shutil
from time import sleep

from scripts.raid_res_import import get_players_sr_and_comments
from scripts.read_write_csv import load_text_file

def print_list(file_list:list,show_identifier:bool=False):
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

def sort_files_attendance_loot_raidres(files:list):
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
        sleep(1)
    except:
        print("Could not auto identify files")
        sleep(1)
        return []
    return sorted_list

def manually_choose_files(input_list:list) -> list:
    sorted_list = []
    print('-'*20)
    print("Which is the loot file?")
    sleep(1)
    print_list(input_list)
    try:
        user_input = int(input("File: "))
        sleep(1)
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

def import_logs() -> tuple[list,list,list,dict]:
    """
    return: sorted list, attendeese, loot log, raidres
    """
    import_list = os.listdir("./Import/")
    sorted_list = sort_files_attendance_loot_raidres(import_list)
    while True:
        if sorted_list != []:
            print_list(sorted_list,True)
            user_input = input("Is this correct ? (y/n): ")
            if user_input == 'y':
                break
            elif user_input == 'n':
                sorted_list = manually_choose_files(sorted_list)
            else:
                print("invalid input")
                print('-'*20)
        else:
            sorted_list = manually_choose_files(import_list)
    
    attendeese = load_text_file(f'./Import/{sorted_list[0][:-4]}')
    loot_log = load_text_file(f'./Import/{sorted_list[1][:-4]}',20)
    raidres = get_players_sr_and_comments(f'{sorted_list[2][:-4]}')
    
    attendeese.sort()

    return sorted_list,attendeese,loot_log,raidres

def safe_imported_logs(filename:str,date:str,logs):

    filepath = f'./Data/Logs-{filename}/Logs'

    if not os.path.exists(filepath):
        os.makedirs(filepath)

    shutil.move(f"./Import/{logs[0]}",f'{filepath}/{filename}_{date}.txt')
    shutil.move(f"./Import/{logs[1]}",f'{filepath}/{filename}_{date}_Loot.txt')
    shutil.move(f'./Import/{logs[2]}',f'{filepath}/{filename}_{date}_{logs[2][-10:]}')
    
    print(f"saved logs in: {filepath}")
    
    