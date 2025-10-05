import general_functions as gen_func
import read_write_csv as rw_csv
import raid_attendance
import manage_dict_func as mg_dict_func

import time
from datetime import datetime

empty_sheet = {'columns': ['Player', 'Item', 'prev_sheet', 'Bonusroll']}

#function to calculate line length for styling the sheet
def get_line_length(row):
    count_columns = len(row)
    line_length = 57 + (count_columns - 3) * 13
    return line_length

def print_sr_plus_sheet(sr_dict):
    line_length = get_line_length(sr_dict["columns"])# get how long the entry is and makes the lines longer for styling
    gen_func.print_line(line_length)    
    for row in sr_dict:
        if sr_dict[row][0] == "Player":
            print(style_row(sr_dict[row]))
            gen_func.print_line(line_length)
        else:
            sr_dict[row] = calc_bonus_roll(sr_dict[row])
            print(style_row(sr_dict[row]))
            gen_func.print_line(line_length)

def style_row(row:list):
    row_to_print = "|"
    column = 0
    column_length = 30
    for value in row:
        #player name
        if column == 0:
            row_to_print += f' {value}{(14 - len(value)) * " "}|'
            column += 1
        #Item
        elif column == 1:
            row_to_print += f'{value}{(column_length - len(value)) * " "}|'
            column += 1

        #bonusroll and numbers
        elif column == 3:
            if value != "Bonusroll":#if you've changed the name of the column change it here to match
                
                value_len = len(str(value))#3
                right_side = (10 - value_len) // 2# 10- 3 = 7 / 2 = 4
                left_side = 10 - value_len - right_side

                row_to_print += f'{left_side * " "}{value}{right_side * " "}|'
                column += 1
            else:    
                row_to_print += f' {value}|'
                column += 1
        #itemrow
        elif column == 2:
            if value == "prev_sheet":#if you've changed the name of the column change it here to match
                row_to_print += f'{value}|'
                column += 1
            else:
                value_len = len(str(value))
                right_side = (10 - value_len) // 2
                left_side = 10 - value_len - right_side
                row_to_print += f'{left_side * " "}{value}{right_side * " "}|'
                column += 1
        #dates only, everything after the fixed columns above
        else:
            spaces = 12 - len(value)
            left = spaces // 2
            right = spaces - left
            row_to_print += f'{left * " "}{value}{right * " "}|'
            column += 1


    return row_to_print

def calc_bonus_roll(row_entry):
    #get player row and make a sum after the fixed columns -> only date columns ~12 -> Quartal
    
    bonus_roll = int(row_entry[2])#get bonus roll from previous sheets
    consecutive_raids_missing = 0
    for entry in range(4,len(row_entry)):
        if row_entry[entry] == "present":
            bonus_roll += 10
            consecutive_raids_missing = 0 #reset to 0
        elif row_entry[entry] == "not":
            #see if the player was missing 2 raids in a row
            #Idea: search player in player dictionary to see if player has attended at least one raid in 1 or 2 weeks to not get the -5
            #not entirely sure where to safe this... maybe add an overall SR sheet that puts the week to true if player attended at least one raid
            consecutive_raids_missing += 1
            if consecutive_raids_missing == 2:
                bonus_roll -= 5 #reset to 0
                consecutive_raids_missing = 0
            #    
        else:
            pass
    #gives the current bonus roll, back into the list -> column 3 "Bonusroll"
    row_entry[3] = bonus_roll
    return row_entry

def find_player_by_char(character_name:str,player_dict:dict) -> str:
    
    for player in player_dict:
        character_list = str(player_dict[player]).split(".")
        if character_name in character_list:
            #rint(f"Player {player} found! with character {user_input}.")
            return player
    print("Player not found in player dictionary")
    return character_name

#loop till every player is in the SR+ sheet
def add_player_to_sheet(player_list:list, sr_plus_dict:dict ,player_dict:dict):
    while player_list != []:

        for player in player_list:

            if mg_dict_func.check_if_player_exists(player,player_dict):
                #Idea: get sr sheet function of main menu intersect with SR sheet export so editor doesnt need to write the item, just choose item 1 or 2 to be the SR+
                print(f"adding {player} to SR+ sheet...")
                sr_plus_item = gen_func.get_user_input(f"{player}s SR+ ?: ")
                gen_func.print_line()
                player_list_part_a = [player, sr_plus_item, 0, 0]
                player_list_part_b = []
                for day in range(0,(len(sr_plus_dict["columns"][4:-1]))):
                    player_list_part_b.append("-") #fill past days with "-" empty space (newly joined player)
                player_list_part_b.append("present") #add new day with "attended"

                player_sr_list = player_list_part_a + player_list_part_b

                sr_plus_dict[player] = player_sr_list
                player_list.remove(player)
                time.sleep(0.5)
            else:
                print(f"Character {player} needs to be added to dict")
                mg_dict_func.add_new_players(player_dict)



#new column for the SR+ Sheet
def make_new_entry(filename,sr_plus_sheet:dict):
    if len(sr_plus_sheet["columns"])  >= 12: #8weeks/raids ~ 2 months
        sr_plus_sheet = make_copy_of_sheet(filename,sr_plus_sheet)
    get_date = gen_func.get_user_input("Raid Date (yyyy-mm-dd): ")
    
    if get_date == 'q':
        return
        
    else:
        print("loading player dictionary...")
        player_dict = rw_csv.read_csv_file_players()
        
        attendese = raid_attendance.get_raid_attendees()
        
        player_attended = [find_player_by_char(character, player_dict) for character in attendese]
        
        sr_plus_sheet["columns"].append(get_date)

        for player in sr_plus_sheet:
            if player != "columns":
                if player in player_attended:
                    player_attended.remove(player)
                    sr_plus_sheet[player].append("present")
                else:
                    sr_plus_sheet[player].append("not")

        if player_attended != []:
            print(f"{player_attended}: need to be added to sheet")
            add_player_to_sheet(player_attended, sr_plus_sheet, player_dict)
            pass #add player to sheet
        rw_csv.safe_sr_sheet_csv(filename,sr_plus_sheet)
    return sr_plus_sheet

def make_copy_of_sheet(filename:str,sr_sheet:dict) -> dict:
    print("make copy of SR+ sheet")
    time.sleep(1)
    #safe file under different name
    date = str(datetime.now().strftime('%Y-%m-%d'))
    filename_safe = f'{date}_{filename}'
    rw_csv.safe_sr_sheet_csv(filename_safe, sr_sheet)
    
    #make new dictionary for new sheet
    new_sr_sheet = empty_sheet

    for player in sr_sheet:
        if player != "columns":
            prev_bonus = int(sr_sheet[player][2]) + int(sr_sheet[player][3])
            print(prev_bonus)
            new_sr_sheet[player] = [sr_sheet[player][0],sr_sheet[player][1],prev_bonus,0]
        else:
            pass
    
    return new_sr_sheet

def create_new_sr_plus_sheet():
    gen_func.print_menu_title("Create New Sheet")
    sr_sheets = rw_csv.load_sr_sheets_directory()
    
    filename = gen_func.get_user_input("new SR+ sheet name: ")
    
    if filename == 'q':
        return
    
    else:
        sr_sheets.append(filename)
        rw_csv.safe_sr_sheets_directory(sr_sheets)
        rw_csv.safe_sr_sheet_csv(filename,empty_sheet)
    gen_func.print_line()

####################### Test Cases ##############################
test_dict_1 = {'columns': ['Player', 'Item', 'prev_sheet', 'Bonusroll', '2025-09-28', '2025-09-21', '2025-09-16'],
               'Gwynn': ['Gwynn', 'Hammer', '0', '30', 'present', 'present', 'present'],
               'Nutbath': ['Nutbath', 'staff of awesomeness', '0', '20', 'present', 'not', 'present']}

test_row = ["Hammer",10,20,"present","present","present","not","not","present","not","present","not"]
test_dict = {"columns":["Player","prev bonus", "bonusroll", "raid", "raid", "raid", "raid", "raid", "raid", "raid", "raid", "raid"],
             "Gwynn": test_row,
             "Player1" : test_row,
             "Player2" : test_row}


#make_new_entry()
#print_sr_plus_sheet(test_dict_1)
#print(f'new bonus + previous: {calc_bonus_roll(test_row)}')
#print(find_player_by_char(str(gen_func.get_user_input("Character")).capitalize()))
