import os, shutil, csv, json
from time import sleep

def load_text_file(filename,cut_text:int = 0):
    
    with open(f'{filename}.txt', newline='') as text_file:
        text_as_list = [line[cut_text:].rstrip("\r\n") for line in text_file]
        return text_as_list

def load_csv(filename:str) -> list:
    csv_file = []
    if filename.endswith(".csv"):
        filename = filename[:-4]
    with open (f'{filename}.csv',newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            csv_file.append(row)
    return csv_file

def load_json(filename:str) -> list:
    filepath = f'{filename}.json'
    
    if not os.path.exists(filepath):
        print("File not found.")
        return []
    else:
        try:
            with open(filepath, "r", encoding="utf-8") as data:
                doc = json.load(data)
            return doc
        except:
            return []

def get_raidres_data(filename:str) -> dict:
    raidres_data = load_csv(f'./Import/{filename}')
    
    keys = list(set([attendee[1] for attendee in raidres_data if attendee[1] != 'Attendee']))
    keys.sort()

    final_raidres_data = {}

    for key in keys:
        items = []
        comments = []
        char_class = ""
        for item in raidres_data:
            if item[1] == key:
                items.append(item[0])
                comments.append(item[3])
                char_class = item[2]
        final_raidres_data.update({key:{'class':char_class, 'items':items, 'comments':comments}})
    
    return final_raidres_data


def save_imported_logs(filename:str,date:str,logs):

    filepath = f'./Data/{filename}/Logs'

    if not os.path.exists(filepath):
        os.makedirs(filepath)

    shutil.move(f"./Import/{logs[0]}",f'{filepath}/{filename}_{date}.txt')
    shutil.move(f"./Import/{logs[1]}",f'{filepath}/{filename}_{date}_Loot.txt')
    shutil.move(f'./Import/{logs[2]}',f'{filepath}/{filename}_{date}_{logs[2][-10:]}')
    
    print(f"saved logs in: {filepath}")

