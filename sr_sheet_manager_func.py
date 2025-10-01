import general_functions

def get_line_length(row):
    count_columns = len(row)
    line_length = 60 + (count_columns - 3) * 13
    return line_length

def print_sr_plus_sheet(sr_dict):
    line_length = get_line_length(sr_dict["columns"])
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
        #bonusroll and numbers
        elif column == 2:
            if value != "Bonusroll":
                row_to_print += f'{4 * " "}{value}{4 * " "}|'
                column += 1
            else:    
                row_to_print += f'{value}{(10 - len(value)) * " "}|'
                column += 1
        #itemrow
        elif column == 1:
            row_to_print += f' {value}{(column_length - len(value)) * " "}|'
            column += 1
        #dates only
        else:
            spaces = 12 - len(value)
            left = spaces // 2
            right = spaces - left
            row_to_print += f'{left * " "}{value}{right * " "}|'
            column += 1


    return row_to_print