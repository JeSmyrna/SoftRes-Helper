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

#not ready to use, just guessing here
def write_csv_raid_softres(raidname,sr_dict):
    with open(f'Data/{raidname + "sr_sheet"}.csv', 'w', newline='') as csvfile:
        fieldnames = ['Player', ''] #Format need to think about
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for entry in sr_dict:
            #characters = str(sr_dict[entry])
            writer.writerow({'Player': f'{entry}'})
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