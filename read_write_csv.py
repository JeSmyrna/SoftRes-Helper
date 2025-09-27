import csv

test_dict = {
    "Gwynni" : "Aepfel",
    "Bernd" : "Buddl Rum"
}

def write_csv_file(dictionary):
    with open('player_chars.csv', 'w', newline='') as csvfile:
        fieldnames = ['Character', 'Soft Reserve A', 'Soft Reserve B']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for entry in dictionary:
            soft_reserve = str(dictionary[entry]).split(",")
            if len(soft_reserve) < 2:
                soft_reserve.append("None")
            writer.writerow({'Character': f'{entry}', 'Soft Reserve A': f'{soft_reserve[0]}', 'Soft Reserve B': f'{soft_reserve[1]}'})

def read_csv_file() -> dict:
    get_dict = {}
    with open('player_chars.csv', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == "Player":
                continue
            else:
                get_dict[row[0]] = row[1]
    return get_dict