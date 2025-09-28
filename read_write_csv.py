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