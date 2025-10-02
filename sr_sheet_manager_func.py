import general_functions as gen_func
import read_write_csv as rw_csv
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
                row_to_print += f'{4 * " "}{value}{4 * " "}|'
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
                row_to_print += f'{5 * " "}{value}{4 * " "}|'
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
        else:
            
            #see if the player was missing 2 raids in a row
            consecutive_raids_missing += 1
            if consecutive_raids_missing == 2:
                bonus_roll -= 5 #reset to 0
                consecutive_raids_missing = 0
                
            else:
                pass
    #gives the current bonus roll, back into the list -> column 3 "Bonusroll"
    row_entry[3] = bonus_roll
    return row_entry

def find_player_by_char(character_name:str) -> str:
    print("loading player dictionary...")
    player_dict = rw_csv.read_csv_file_players()
    
    for player in player_dict:
        character_list = str(player_dict[player]).split(".")
        if character_name in character_list:
            #rint(f"Player {player} found! with character {user_input}.")
            return player
    print("Player not found in player dictionary")



####################### Test Cases ##############################
test_dict_1 = {'columns': ['Player', 'Item', 'prev_sheet', 'Bonusroll', '2025-09-28', '2025-09-21', '2025-09-16'],
               'Gwynn': ['Gwynn', 'Hammer', '0', '0', 'present', 'present', 'present'],
               'Wilfret': ['Wilfret', 'staff of awesomeness', '0', '0', 'present', 'not', 'present']}

test_row = ["Hammer",10,20,"present","present","present","not","not","present","not","present","not"]
test_dict = {"columns":["Player","prev bonus", "bonusroll", "raid", "raid", "raid", "raid", "raid", "raid", "raid", "raid", "raid"],
             "Gwynn": test_row,
             "Player1" : test_row,
             "Player2" : test_row}
#print_sr_plus_sheet(test_dict_1)
#print(f'new bonus + previous: {calc_bonus_roll(test_row)}')
#print(find_player_by_char(str(gen_func.get_user_input("Character")).capitalize()))