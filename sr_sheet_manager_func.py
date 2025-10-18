import general_functions as gen_func
import read_write_csv as rw_csv
import raid_attendance
import raid_res_import
import manage_dict_func as mg_dict_func

import time
from datetime import datetime

empty_sheet = {'columns': ['Player', 'Item', 'prev_sheet', 'Bonusroll']}

#function to calculate line length for styling the sheet
def get_line_length(row):
    count_columns = len(row)
    if count_columns > 10:
        line_length = 72 + (10 - 3) * 13
        return line_length
    else:
        line_length = 72 + (count_columns - 3) * 13
        return line_length

def print_sr_plus_sheet(sr_dict) -> dict:
    line_length = get_line_length(sr_dict["columns"])# get how long the entry is and makes the lines longer for styling
    gen_func.print_line(line_length)    
    
    list_to_long = False
    adjusted_list_view = []
    if len(sr_dict['columns']) > 10:
        list_to_long = True
    else:
        pass
    
    for row in sr_dict:
        if sr_dict[row][0] == "Player":
            
            if list_to_long:    
                adjusted_list_view.extend(sr_dict[row][0:4]) #Player,Item,prev,bonusroll
                adjusted_list_view.extend(sr_dict[row][-6:]) #last 6 days
                
                print(style_row(adjusted_list_view,True))
                gen_func.print_line(line_length)

            else:
                print(style_row(sr_dict[row],True))
                gen_func.print_line(line_length)
        else:
            sr_dict[row] = calc_bonus_roll(sr_dict[row])
            
            if list_to_long:
                adjusted_list_view.clear()
                adjusted_list_view.extend(sr_dict[row][0:4])
                adjusted_list_view.extend(sr_dict[row][-6:])
                
                print(style_row(adjusted_list_view))
                gen_func.print_line(line_length)
            else:
                print(style_row(sr_dict[row]))
                gen_func.print_line(line_length)
    return sr_dict

def style_row(row:list, header:bool = False):
    row_to_print = "|"
    column = 0
    column_length = 45
    for value in row:
        #player name
        if column == 0:
            row_to_print += f' {value}{(14 - len(value)) * " "}|'
            column += 1
        #Item
        elif column == 1:
            item_name = str(value).strip('"')
            row_to_print += f'{item_name}{(column_length - len(item_name)) * " "}|'
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
            right = spaces // 2
            left = spaces - right
            
            if value == 'present':
                row_to_print += f'{left * " "}{gen_func.color_text(value,'gr')}{right * " "}|'
            elif value == 'absent':
                row_to_print += f'{left * " "}{gen_func.color_text(value,'rd')}{right * " "}|'
            else:
                row_to_print += f'{left * " "}{value}{right * " "}|'
            column += 1

    if header != True:
        return row_to_print
    else:
        return gen_func.color_text(row_to_print,'blwb')

def calc_bonus_roll(row_entry:list) -> list:
    #get player row and make a sum after the fixed columns -> only date columns ~12 -> Quartal
    
    bonus_roll = int(row_entry[2])#get bonus roll from previous sheets
    consecutive_raids_missing = 0
    for entry in range(4,len(row_entry)):
        if row_entry[1] != 'Nothing':
            if row_entry[entry] == "present":
                bonus_roll += 10
                consecutive_raids_missing = 0 #reset to 0
            elif row_entry[entry] == "absent":
                #see if the player was missing 2 raids in a row
                #Idea: search player in player dictionary to see if player has attended at least one raid in 1 or 2 weeks to not get the -5
                #not entirely sure where to safe this... maybe add an overall SR sheet that puts the week to true if player attended at least one raid
                consecutive_raids_missing += 1
                if consecutive_raids_missing == 2:
                    bonus_roll -= 5 #reset to 0
                    consecutive_raids_missing = 0
                    if bonus_roll <= 0:
                        bonus_roll = 0
                #    
            else:
                pass
        else:
            pass
    #gives the current bonus roll, back into the list -> column 3 "Bonusroll"
    row_entry[3] = bonus_roll
    return row_entry

def find_player_by_char(character_name:str,player_dict:dict) -> str:
    
    for player in player_dict:
        character_list = str(player_dict[player]).split(".")
        if character_name in character_list:
            #print(f"Player {player} found! with character {user_input}.")
            return character_name #player - just return charactername
    print(f"Player {character_name} not found in player dictionary")
    return character_name

def add_players_manual_to_sheet(filename,sr_plus_dict:dict) -> dict:
    
    player_dict = rw_csv.read_csv_file_players()
    gen_func.print_menu_title("Players and Characters")
    mg_dict_func.print_dictionary(player_dict)
    
    #gen_func.print_menu_title("SR+ Sheet")
    #print_sr_plus_sheet(sr_plus_dict)

    #print("^^^^ List of players and the SR+ sheet printed above ^^^^")
    time.sleep(1)

    while True:

        player_name = input("Add Player: ").capitalize()
        if player_name == "Q":
            print("going back...")
            time.sleep(1)
            return
        
        elif mg_dict_func.check_if_player_exists(player_name,player_dict):
            
            if player_name in sr_plus_dict:
                print("player already in SR+ Sheet")
                gen_func.print_line(20)

            else:
                gen_func.print_line(20)
                sr_item = input("SR+ Item: ").capitalize()
                
                attended = input(f'{player_name} attended last raid ? (y/n): ')
                if attended == "y":
                    attended = True
                else:
                    attended = False

                ask_permission = input(f'Add "{player_name}" and their SR+ "{sr_item}" to the SR+ Sheet ? (y/n) ')

                if ask_permission == "y":
                    list_start = [player_name, sr_item, 0, 0]
                    list_complete = fill_past_days(list_start, sr_plus_dict, attended)
                    sr_plus_dict[player_name] = list_complete
                    rw_csv.safe_sr_sheet_csv(filename,sr_plus_dict)
                    print("file is safed")
                    time.sleep(1)
                    return #sr_plus_dict

                elif ask_permission == "n":
                    print("not adding player...")
                    gen_func.print_line()

                elif ask_permission == "q":
                    gen_func.print_line()
                    return
                
                else:
                    print("invalid input")

        else:
            print(f'{player_name} not found...')
            player_dictionary_name = find_player_by_char(player_name,player_dict)
            print(f'Did you mean player: {player_dictionary_name}? - {player_name} might be an alt')
            time.sleep(1)
            gen_func.print_line()
def fill_just_past_days(list_part_a:list, sr_plus_sheet:dict) -> list:
    list_part_b = []
    for day in range(0,(len(sr_plus_sheet["columns"][4:]))):
        list_part_b.append("-")
    
    player_sr_list = list_part_a + list_part_b
    return player_sr_list

def fill_raid_day_attendance(attendance:list,sr_plus_sheet:dict):
    ask_user_date = input('Raid Date - yyyy-mm-dd: ')
    get_keys = sr_plus_sheet.keys()

    for player in get_keys:
        if player == 'columns':
            row = sr_plus_sheet['columns']
            row.append(ask_user_date)
            sr_plus_sheet.update({'columns':row})
        else:
            row = sr_plus_sheet.get(player)
            if player in attendance:
                row.append('present')
                sr_plus_sheet.update({player:row})
            else:
                row.append('absent')
                sr_plus_sheet.update({player:row})

def fill_past_days(list_part_a:list, sr_plus_dict:dict, attended_last_raid:bool = True) -> list:
    
    list_part_b = []
    if len(sr_plus_dict['columns']) <= 4:
        return list_part_a
    
    for day in range(0,(len(sr_plus_dict["columns"][4:-1]))):
        list_part_b.append("-") #fill past days with "-" empty space (newly joined player)
    
    #scratched to record attendance, but have to change the calc_bonus_roll func
    #if list_part_a[1] == "Nothing":
        #list_part_b.append("-")
    else:
        if attended_last_raid:
            list_part_b.append("present") #add new day with "attended"
        else:
            list_part_b.append("absent")

    player_sr_list = list_part_a + list_part_b
    return player_sr_list


#loop till every player is in the SR+ sheet
def add_players_to_sheet(player_list:list, sr_plus_dict:dict ,player_dict:dict):
    while player_list != []:

        for player in player_list:

            if mg_dict_func.check_if_player_exists(player,player_dict):
                
                print(f"adding {player} to SR+ sheet...")

                sr_plus_item = f'{find_choose_sr_plus(player,player_dict)}'

                gen_func.print_line()

                player_list_part_a = [player, sr_plus_item, 0, 0]
                player_sr_list = fill_past_days(player_list_part_a,sr_plus_dict,True)

                sr_plus_dict[player] = player_sr_list
                player_list.remove(player)
                time.sleep(0.5)
            else:
                print(f"Character {player} needs to be added to dict")
                mg_dict_func.add_new_players(player_dict)
                rw_csv.write_csv_file_players(player_dict)

#delete player, add to log, make note that it got deleted + when
def delete_player_manually_from_sheet(filename:str, sr_plus_sheet:dict):
    award_sr_plus(filename,sr_plus_sheet,True)
    
def find_choose_sr_plus(player:str,player_dict:dict) -> str: #player name 
    attendeese = raid_attendance.get_raid_attendees()
    #raidres = raid_res_import.get_soft_reserve_players()
    raidres = raid_res_import.get_players_sr_and_comments()
    
    attended_players, not_attended_players = raid_attendance.intersect_raidres_and_attendees(attendeese,raidres)
    items = attended_players.get(player)
    if items == None:
        return 'Nothing'

    else:
        print(f'{gen_func.color_text(player,'yw')} raidres: {gen_func.color_text(items[0],'yw')} and {gen_func.color_text(items[1],'yw')}')
        longest_item = max([len(items[0]),len(items[1])]) + 5
        print(f"""
[1] {items[0]}{(longest_item - len(items[0])) * ' '}- "{items[2]}"
[2] {items[1]}{(longest_item - len(items[1])) * ' '}- "{items[3]}"
[3] Nothing
""")
        while True:
                user_input = input(f"Choose SR+ for {gen_func.color_text(player,'yw')}?: ")
                
                if user_input == "1":
                    return items[0]
                elif user_input == "2":
                    return items[1]
                elif user_input == "3":
                    return "Nothing"
                else:
                    print("invalid input")

def award_sr_plus(filename:str, sr_plus_sheet:dict,delete_sr:bool = False):
    gen_func.print_menu_title("SR+ Sheet")
    print_sr_plus_sheet(sr_plus_sheet)
    gen_func.print_line()
    
    #change question for deletion or awarding
    msg_1 = ''
    if delete_sr:
        msg_1 = 'Which player SR+ should be deleted?: '
    else:
        msg_1 = "Which player got their SR+?: "

    #choose players till satisfied
    while True:
        user_entry = input(msg_1).capitalize()
        if user_entry == "Q":
            print("going back...")
            time.sleep(1)
            return
        elif user_entry in sr_plus_sheet:
            
            #change question for deletion or awarding
            msg_2 = ''
            if delete_sr:
                msg_2 = f'Delete Player "{gen_func.color_text(user_entry,'yw')}" and their SR+ "{gen_func.color_text(sr_plus_sheet[user_entry][1],'yw')}" ?: (y/n)'
            else:
                msg_2 = f'Player "{gen_func.color_text(user_entry,'yw')}" have won their SR+ "{gen_func.color_text(sr_plus_sheet[user_entry][1],'yw')}" on the "{gen_func.color_text(sr_plus_sheet["columns"][-1],'yw')}"? (y/n): '

            user_entry_1 = input(msg_2)
            
            if user_entry_1 == "y":

                #note that it got deleted or date aquired
                if delete_sr:
                    note_message = 'deleted'
                else:
                    note_message = '(manual) aquired'

                move_to_loot_log([filename,sr_plus_sheet[user_entry],note_message,sr_plus_sheet["columns"][-1]])

                sr_plus_sheet.pop(user_entry)
                rw_csv.safe_sr_sheet_csv(filename,sr_plus_sheet)
                print("entry has been moved to the sr_awarded_log.csv")
                time.sleep(1)
                gen_func.print_line(20)
                pass

            elif user_entry_1 == "n":
                gen_func.print_line(20)
                pass
            else:
                print("invalid input")
        else:
            print("couldn't find player")
            gen_func.print_line(20)

def award_through_loot_log(filename:str, sr_plus_sheet:dict):
    gen_func.print_menu_title("Award through Loot Log")
    text_file = rw_csv.load_text_file('loot_log',20)
    final_loot_log = []

    #special cases - crafting items
    exception_list = ['Formula','Recipe','Plans']

    for line in text_file:
        edited_line = line.split(": ")
        #catch special naming conventions for carfting items
        if edited_line[0] in exception_list:
            item_name = ': '.join([edited_line[0],edited_line[1]])
            edited_line = [item_name,edited_line[-1]]
        traded_line = edited_line[1].split(" > ")
        edited_line.pop(1)
        if len(traded_line) > 1:
            print(f'{gen_func.color_text(traded_line[0],'rd')} traded "{gen_func.color_text(edited_line[0],'yw')}" to {gen_func.color_text(traded_line[1],'gr')}')
            edited_line.insert(0,traded_line[1])
            time.sleep(1)
            final_loot_log.append(edited_line)
        else:
            edited_line.insert(0,traded_line[0])
            final_loot_log.append(edited_line)

    #look for players in SR sheet with loot log
    sr_sheet_keys = sr_plus_sheet.keys()
    players_and_chars = rw_csv.read_csv_file_players()
    found_a_srplus_loot = False
    list_of_players = []

    for entry in final_loot_log:
        name = find_player_by_char(entry[0],players_and_chars)
        
        if name in sr_sheet_keys and entry[1] == sr_plus_sheet[name][1]:
            
            print(f'{gen_func.color_text(name,'rd')} found: {gen_func.color_text(entry[1],'yw')} dropped on the {gen_func.color_text(sr_plus_sheet['columns'][-1],'gr')} and player {gen_func.color_text(name,'rd')} won the loot')
            while True:
                user_input = input('Move to loot log? (y/n): ')
                if user_input == 'y':
                    found_a_srplus_loot = True
                    list_of_players.append(name)
                    move_to_loot_log([filename,sr_plus_sheet[name],'aquried through loot log ',sr_plus_sheet["columns"][-1]],True)
                    sr_plus_sheet.pop(name)
                    break
                elif user_input == 'n':
                    print('moving on...')
                    time.sleep(1)
                    break
                else:
                    print('invalid input')
                    time.sleep(1)
            gen_func.print_line(20)

        else:
            pass

    rw_csv.safe_sr_sheet_csv(filename,sr_plus_sheet)
    if found_a_srplus_loot:
        print("entries have been moved to the sr_awarded_log.csv")
        time.sleep(1)
        print(f"No more SR+ awarded loot found. Congratulations to {gen_func.color_text(', '.join(list_of_players),'yw')}")
        time.sleep(1)
    else:
        print(f'No SR+ awarded for {filename} on the {sr_plus_sheet["columns"][-1]}...')
        time.sleep(1)

def move_to_loot_log(player:list,malus:bool = False):
    """
    List items that are needed:

    player[0] = filename\n
    player[1] = all entries (row) in sheet of mentioned player\n
    player[2] = log note or message, why it was moved\n
    player[3] = last day in dict["columns"][-1]\n
    """
    #make new format: player = [filename,[all columns],log_message,date_aquired]
    
    log_file = rw_csv.load_sr_awarded_log()
    log_entry_num = len(log_file)

    filename = player[0]
    player_name = player[1][0]
    sr_item = player[1][1]
    bonus_roll = int(player[1][3])#because of awarding through log
    if malus:
        bonus_roll -= 10
    log_note = player[2]
    date_added_to_log = gen_func.get_date()

    new_log_row = [log_entry_num,filename,player_name,sr_item,bonus_roll,log_note,date_added_to_log]
    rw_csv.safe_sr_awarded_log(new_log_row)

def make_entry(filename:str,sr_plus_sheet:dict):
    gen_func.print_menu_title('Make New Entry')
    print('''Have the files been updated for the new raid?
raidres.txt
attendeese.txt
loot_log.txt''')
    
    #make sure user updated all the docs
    gen_func.print_line(10)
    ask_user = input('(y/n): ')
    if ask_user == 'y':
        attendeese = raid_attendance.get_raid_attendees()
        player_dict = rw_csv.read_csv_file_players()
        #raidres = raid_res_import.get_soft_reserve_players()
        raidres = raid_res_import.get_players_sr_and_comments()
        pass
    else:
        print('going back...')
        time.sleep(1)
        return

    #check if attendeese in player dict
    char_in_dict = []
    while attendeese != []:
        all_characters = player_dict.items()
        for character in attendeese:
            for char_list in all_characters:
                char_list = str(char_list[1]).split('.')
                if character in char_list:  
                    char_in_dict.append(character)
                    attendeese.remove(character)
                    break
            else:
                mg_dict_func.add_new_player(character,player_dict)
    char_in_dict.sort()
    
    #check if player has already a character in SR+ Sheet
    for char_id in range(len(char_in_dict)):
        char = char_in_dict[char_id]
        #print(sr_plus_sheet.keys())
        if char not in sr_plus_sheet.keys():
            #check if player has alts in sheet
            is_in,char_in,data = check_if_alt_in_sheet(char,sr_plus_sheet)
            if is_in:
                try:
                    raid_res_item_list = raidres[char]
                except KeyError:
                    print('couldnt find key')
                except:
                    print('something else must ve gone wrong')

                #check if player alt doesn't accumulates Bonus roll for the other chars SR+
                if data[1] not in raid_res_item_list:
                    #print(data[1],' - ',raid_res_item_list)
                    print(f'Player of {gen_func.color_text(char,'yw')} did not reserve the same item as their alt {gen_func.color_text(char_in,'yw')}')
                    time.sleep(1)
                    print(f'Player has already {gen_func.color_text(char_in,'yw')} in sheet. SR+ {gen_func.color_text(data[1],'yw')} with a {gen_func.color_text('Bonusroll','gr')} of {gen_func.color_text(data[3],'yw')}')
                    while True:
                        ask_user_1 = input(f'{gen_func.color_text('Replace entry','rd')}, with character {gen_func.color_text(char,'yw')}? (y/n): ')
                        if ask_user_1 == 'y':
                            print('moving to log')
                            time.sleep(1)
                            move_to_loot_log([filename,data,f'{char} replaced {char_in}',sr_plus_sheet['columns'][-1]])
                            sr_plus_sheet.pop(char_in)
                            gen_func.print_line(10)
                            new_sr_item = f'{find_choose_sr_plus(char,player_dict)}'
                            new_sr_entry = fill_just_past_days([char,new_sr_item,0,0],sr_plus_sheet)
                            sr_plus_sheet.update({char:new_sr_entry})
                            break

                        elif ask_user_1 == 'n':
                            char_in_dict[char_id] = char_in
                            raidres.update({char_in:raidres.get(char)})
                            break
                        else:
                            print('invalid input')

                #player alt has the same SR+            
                else:
                    char_in_dict[char_id] = char_in
                    raidres.update({char_in:raidres.get(char)})
            else:
                gen_func.print_line(10)
                new_sr_item = f'{find_choose_sr_plus(char,player_dict)}'
                new_sr_entry = fill_just_past_days([char,new_sr_item,0,0],sr_plus_sheet)
                sr_plus_sheet.update({char:new_sr_entry})
        
        #finds char in SR+ Sheet
        else:
            print(f'found {char} in SR+ Sheet')
            #print((sr_plus_sheet[char][1]),' - ',raidres.get(char))
            
            try:
                if sr_plus_sheet[char][1] == 'Nothing':
                    pass

                elif str(sr_plus_sheet[char][1]) not in raidres.get(char):
                    print(f"Player {gen_func.color_text(char,'yw')} didn't reserve the same SR+")
                    ask_user_2 = input('Choose new SR+ ? (y/n): ')
                    while True:
                        if ask_user_2 == 'y':
                            print('moving to log')
                            time.sleep(1)
                            move_to_loot_log([filename,sr_plus_sheet[char],f'{char} choose new SR+',sr_plus_sheet['columns'][-1]])
                            sr_plus_sheet.pop(char)
                            gen_func.print_line(10)
                            new_sr_item = f'{find_choose_sr_plus(char,player_dict)}'
                            new_sr_entry = fill_just_past_days([char,new_sr_item,0,0],sr_plus_sheet)
                            sr_plus_sheet.update({char:new_sr_entry})
                            break
                        elif ask_user_2 == 'n':
                            break
                        else:
                            print('try again')
                else:
                    pass
            except:
                print(f'{char} not in raidres found')

    gen_func.print_line(10)

    #func to ask for new day and add to every entry the attendance
    fill_raid_day_attendance(char_in_dict,sr_plus_sheet)
    print('Saving SR+ Sheet...')
    time.sleep(1)
    sr_plus_sheet = print_sr_plus_sheet(sr_plus_sheet)
    rw_csv.safe_sr_sheet_csv(filename,sr_plus_sheet)

    #add func to check loot log before adding new entry
    gen_func.print_line(10)
    print('Looking through loot log...')
    time.sleep(1)
    award_through_loot_log(filename,sr_plus_sheet)
    sr_plus_sheet = print_sr_plus_sheet(sr_plus_sheet)
    rw_csv.safe_sr_sheet_csv(filename,sr_plus_sheet)

    return sr_plus_sheet

def check_if_alt_in_sheet(character:str,sr_sheet:dict) -> tuple[bool,str,list]:
    player_dict = rw_csv.read_csv_file_players()
    all_characters = player_dict.items()
    print(f'searching player {character}')
    for char_list in all_characters:
        char_list = str(char_list[1]).split('.')
        if character in char_list:
            for char in char_list:
                if char in sr_sheet.keys():
                    return True,char,sr_sheet[char]
    else:
        return False,character,[]

#make_entry('Test',rw_csv.load_sr_sheet('Test'))
def find_double_chars(attendeese:list,player_dict:dict) -> list:

    dict_keys = list(player_dict.keys())
    dict_keys.sort()
    new_player_dict = {}
    for key in dict_keys:
        char_list = str(player_dict.get(key)).split('.')
        new_player_dict.update({key:char_list})
        
    no_doubles = []
    for attendee in attendeese:
        for char_list in new_player_dict:
            if attendee in new_player_dict[char_list]:
                if new_player_dict[char_list][-1] != True:
                    no_doubles.append(attendee)
                    add_bool_list = new_player_dict[char_list].append(True)
                else:
                    pass
    return no_doubles
#new column for the SR+ Sheet
def make_new_entry(filename,sr_plus_sheet:dict):
    #if len(sr_plus_sheet["columns"])  >= 9: #4col for player, 1col for last day of last sheet, 4 days = 9
    #    sr_plus_sheet, old_sheet = make_copy_of_sheet(filename,sr_plus_sheet)
        #print(sr_plus_sheet)
    get_date = gen_func.get_user_input("Raid Date (yyyy-mm-dd): ")
    
    if get_date == 'q':
        return
        
    else:
        print("loading player dictionary...")
        player_dict = rw_csv.read_csv_file_players()
        
        attendese = raid_attendance.get_raid_attendees()
        
        #change character name to player name
        #player_attended = [find_player_by_char(character, player_dict) for character in attendese]
        
        sr_plus_sheet["columns"].append(get_date)

        for player in sr_plus_sheet:
            if player != "columns":
                if player in attendese:
                    attendese.remove(player)
                    sr_plus_sheet[player].append("present")
                else:
                    sr_plus_sheet[player].append("absent")
                #new calced prev bonus = calculate(old_sheet[player][5:] + sr_plus_sheet[player][6])
                #sr_plus_sheet[player][3] = difference old prev bonus new prev bonus ?
                
        if attendese != []:
            print(f"{attendese}: need to be added to sheet")
            add_players_to_sheet(attendese, sr_plus_sheet, player_dict)
            pass #add player to sheet
        
    print_sr_plus_sheet(sr_plus_sheet)
    rw_csv.safe_sr_sheet_csv(filename,sr_plus_sheet)
    
    return sr_plus_sheet

def make_copy_of_sheet(filename:str,sr_sheet:dict) -> dict:
    print("make copy of SR+ sheet")
    time.sleep(1)
    
    #safe file under different name
    date = str(datetime.now().strftime('%Y-%m-%d'))
    filename_safe = f'{date}_{filename}'
    rw_csv.safe_sr_sheet_csv(filename_safe, sr_sheet)
    new_sr_sheet = {}
    
    #make new dictionary for new sheet - add last day to new sheet
    last_day = sr_sheet['columns'][-1]
    blueprint = empty_sheet["columns"].copy()
    #blueprint.append(last_day)

    new_sr_sheet['columns'] = blueprint
    
    for player in sr_sheet:
        if player != "columns":
            prev_bonus = int(sr_sheet[player][3])
            print(prev_bonus)
            new_sr_sheet[player] = [sr_sheet[player][0],sr_sheet[player][1],prev_bonus,0]#,sr_sheet[player][-1]]
        else:
            pass
    
    return new_sr_sheet, sr_sheet

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

#award_sr_plus("Test",test_dict_1)
#add_players_manual_to_sheet(test_dict_1)
#make_new_entry()
#print_sr_plus_sheet(test_dict_1)
#print(f'new bonus + previous: {calc_bonus_roll(test_row)}')
#print(find_player_by_char(str(gen_func.get_user_input("Character")).capitalize()))
