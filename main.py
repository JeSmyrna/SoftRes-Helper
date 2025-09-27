import raid_attendance
import raid_res_import
import read_write_csv
import manage_dict_func
import time

print_line = "-" * 50

menu_options = [
    "[0] Quit program",
    "[1] get intersection.csv from raid res and attendeese",
    "[2] add more players",
    "[3] print dict"
                ]

player_dict = {}

def get_intersect():
    while True:
        user_entry = input("Updated >raidres.txt< and >attendeese.txt< ? (y/n): ")
        if user_entry == "y":
            raid_res_dict = raid_res_import.get_soft_reserve_players()
            attendeese_list = raid_attendance.get_raid_attendees()

            attended_players, not_attended_players = raid_attendance.intersect_raidres_and_attendees(attendeese_list,raid_res_dict)
            #print("-" * 20 + "Attended" + "-" * 20)
            #print_dictionary(attended_players)
            #print("-" * 20 + "Not Attended" + "-" * 20)
            #print_dictionary(not_attended_players)

            read_write_csv.write_csv_file(attended_players)

            break
        
        elif user_entry == "n":
            print("Pls update >raidres.txt<")
            time.sleep(3)
            break
        else:
            print("Input not recognized")       

def print_dictionary(dictionary:dict):
    print("-" * 20 + "Player Dictionary" + "-" * 20)
    for player in dictionary:
        if len(player) < 16:
            space = 16 - len(player)
            player_list = str(dictionary[player]).split(".")
            player_characters = ""
            if len(player_list) > 1:
                for name in player_list:
                    player_characters += name + " - "
                player_characters = player_characters[:-3]
                
            print(f"Player: {player}{" " * space}| Characters: {player_characters}")
        else:
            print(f"Player: {player} | Characters: {dictionary[player]}")
    print(print_line)

def mainloop():
    print("Loading players...")
    player_dict = read_write_csv.read_csv_file()
    #print(print_dictionary(player_dict))

    while True:
        for menu_opt in menu_options:
            print(menu_opt)
        print(print_line)
        user_entry = input("Option: ")

        try:
            user_entry = int(user_entry)
            print(print_line)

            if user_entry == 0:
                print("Quitting program...")
                time.sleep(2)
                break

            elif user_entry == 2:
                manage_dict_func.add_new_players(player_dict)
                read_write_csv.write_csv_file(player_dict)

            elif user_entry == 3:
                print_dictionary(player_dict)
        except:
            print("invalid option")
mainloop()