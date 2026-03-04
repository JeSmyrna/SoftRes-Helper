import json

def save_json(filename:str,data:list):
    path = f'{filename}.json'

    with open(path, "w", encoding="utf-8") as data_dump:
        json.dump(data,data_dump,indent=4)

def save_text(filename:str, text_data:list, override:bool = True):
    path = f'{filename}.txt'
    write_mode = ""

    if override:
        write_mode = "w"
    else:
        write_mode = "a"

    with open(path, 'a') as sr_directory:
        for sheet_name in text_data:
            sr_directory.write(f'\n{sheet_name}')