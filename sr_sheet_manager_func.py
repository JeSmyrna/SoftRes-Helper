import general_functions

#function to calculate line length for styling the sheet
def get_line_length(row):
    count_columns = len(row)
    line_length = 60 + (count_columns - 3) * 13
    return line_length

def print_sr_plus_sheet(sr_dict):
    line_length = get_line_length(sr_dict["columns"])# get how long the entry is and makes the lines longer for styling
    general_functions.print_line(line_length)    
    for row in sr_dict:
        print(style_row(sr_dict[row]))
        general_functions.print_line(line_length)

def style_row(row):
    column_length = 30
    row_to_print = "|"
    column = 0

    for value in row:
        #player name
        if column == 0:
            row_to_print += f' {value}{(14 - len(value)) * " "}|'
            column += 1
        #prev_sheet column, bonus rolls from older sheets
        elif column == 2:
            if value != "prev_sheet":#if you've changed the name of the column change it here to match
                row_to_print += f'{5 * " "}{value}{4 * " "}|'
                column += 1
            else:    
                row_to_print += f'{value}{(10 - len(value)) * " "}|'
                column += 1

        #bonusroll and numbers
        elif column == 3:
            if value != "Bonusroll":#if you've changed the name of the column change it here to match
                row_to_print += f'{4 * " "}{value}{4 * " "}|'
                column += 1
            else:    
                row_to_print += f'{value}{(10 - len(value)) * " "}|'
                column += 1
        #itemrow
        elif column == 1:
            row_to_print += f' {value}{(column_length - len(value)) * " "}|'
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
    
    bonus_roll = row_entry[1]#get bonus roll from previous sheets
    consecutive_raids_missing = 0
    for entry in range(2,len(row_entry)):
        if row_entry[entry] == "present":
            bonus_roll += 10
            consecutive_raids_missing = 0 #reset to 0
        else:
            
            #see if the player was missing 2 raids in a row
            consecutive_raids_missing += 1
            if consecutive_raids_missing == 2:
                bonus_roll -= 5
                consecutive_raids_missing = 0 #reset to 0
            else:
                pass
    #gives the current bonus roll back into the list -> column 3 "Bonusroll"
    row_entry[2] = bonus_roll
    return row_entry

test_row = ["Hammer",10,20,"present","present","present","not","not","present","not","present","not"]
print(f'new bonus + previous: {calc_bonus_roll(test_row)}')