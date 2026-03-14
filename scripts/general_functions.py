from datetime import datetime


line_length = 50

def print_line(line_length = 50):
    print("-" * line_length)

def print_menu_title(title):
    max_length = line_length - len(title)
    left_line = max_length // 2
    right_line = max_length - left_line
    print("-" * left_line + title + right_line * "-")

def print_loaded_file(filename):
    message = "Loaded: "
    max_length = line_length - len(filename) - len(message)
    print("-" * max_length + message + color_text(filename,'yw'))

def get_user_input(question:str):
    user_input = input(f"{question}: ")
    return user_input

def get_date() -> str:
    """
    YYYY-MM-DD
    """
    date = str(datetime.now().strftime('%Y-%m-%d'))
    return date

def color_text(text:str,color:str) -> str:
    """
    Red = rd\n
    Yellow = yw\n
    Green = gr\n
    Blue = bl\n
    Black text on white background = blwb
    """
    if color == "rd":
        colored_text = f'\33[31m{text}\033[0m'
        return colored_text
    elif color == "yw":
        colored_text = f'\033[93m{text}\033[0m'
        return colored_text
    elif color == "gr":
        colored_text = f'\33[92m{text}\033[0m'
        return colored_text
    elif color == "bl":
        colored_text = f'\33[94m{text}\033[0m'
        return colored_text
    elif color == "blwb":
        colored_text = f'\33[7m{text}\033[0m'
        return colored_text
    else:
        print("color option: rd, yw, gr, bl, blwb")

def order_dict_alphabetically(dictionary:dict) -> dict:
    
    dict_keys = list(dictionary.keys())
    dict_keys.sort()

    if 'columns' in dict_keys:
        dict_keys.remove('columns')
        dict_keys.insert(0,'columns')

    sorted_dict = {}
    for key in dict_keys:
        sorted_dict.update({key:dictionary[key]})
    return sorted_dict


def sort_dict_by(dictionary:dict, slice_to:int) -> dict:
    descend = False
    dict_index = 0
    key_list = dictionary["columns"][0:slice_to]
    dict_copy = dictionary.copy()
    removed_header = dict_copy.pop("columns")

    while True:
        for cat in key_list:
            print(f'[{dict_index}] - {cat}')
            dict_index += 1

        try:
            user_input = int(input("option: "))
        except ValueError:
            print("Input needs to be a number")
        except:
            print("What?")

        if user_input < len(key_list) and user_input >= 0:
            break

    menu_opt = ["[0] back",
                "",
                ["[1] Ascending",
                 "[2] Descending"]]
    while True:
        
        for opt in menu_opt:
            print(opt)
        input_sorting = input("option: ")
        
        if input_sorting == "0":
            return
        elif input_sorting == "1":
            break
        elif input_sorting == "2":
            descend = True
            break
        else:
            print("not an option")
            print_line(10)

    sorted_dict = {}
    sorted_dict.update({"columns":removed_header})
    try:
        sorted_dict.update(sorted(dict_copy.items(), key=lambda item: item[1][user_input],reverse=descend))
    except:
        print("????")
        return dictionary

    """ for entry in sorted_dict:
        print(sorted_dict[entry][0:4]) """
    
    return sorted_dict