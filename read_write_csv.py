import csv

def write_csv_file_players(dictionary):
    with open('Data/player_chars.csv', 'w', newline='') as csvfile:
        fieldnames = ['Player', 'Characters']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for entry in dictionary:
            characters = str(dictionary[entry])
            writer.writerow({'Player': f'{entry}', 'Characters': f'{characters}'})

def read_csv_file_players() -> dict:
    get_dict = {}
    with open('Data/player_chars.csv', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == "Player":
                continue
            else:
                get_dict[row[0]] = row[1]
    return get_dict

def load_sr_sheet(filename):
    sr_sheet_dict = {}
    try:
        with open(f'Data/{filename}.csv', newline='') as file:
            reader = csv.reader(file)
            rows = 0
            for row in reader:
                if rows == 0:
                    sr_sheet_dict["columns"] = row
                    rows += 1
                else:
                    sr_sheet_dict[row[0]] = row        
        return sr_sheet_dict
    except:
        print("file does not exist")
        return sr_sheet_dict

def load_sr_sheets_directory():
    list_of_sheets = []
    with open(f'Data/raid_directory.txt', newline='') as sr_directory:
        list_of_sheets = [line.rstrip("\r\n") for line in sr_directory]
        return list_of_sheets
    
def safe_sr_sheets_directory(sr_sheet_directory:list):
    with open(f'Data/raid_directory.txt', 'w') as sr_directory:
        for sheet_name in sr_sheet_directory:
            sr_directory.write(f'{sheet_name}\n')
    

def safe_sr_sheet_csv(raidname:str,sr_dict:dict):
    with open(f'Data/{raidname}.csv', 'w', newline='') as csvfile:
        fieldnames = sr_dict["columns"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        column_list = []
        for column_name in sr_dict['columns']:
            column_list.append(column_name)

        dict_row = {}
        for entry in sr_dict:
            if entry != 'columns':
                get_entries = sr_dict[entry]
                for index in range(len(get_entries)):
                    dict_row[column_list[index]] = get_entries[index]
        
                writer.writerow(dict_row)