import raid_attendance
import raid_res_import
import read_write_csv
import manage_dict_func
import sr_sheet_manager
import general_functions
import time



menu_options = [
    "[0] Quit program",
    "[1] get intersection.csv from raid res and attendeese",
    "[2] add more players or characters",
    "[3] delete player or characters",
    "[4] print dict",
    "[5] Manage SR+ Sheet"
                ]

player_dict = {}

def get_intersect():
    while True:
        user_entry = input("Updated >raidres.txt< and >attendeese.txt< ? (y/n): ")
        if user_entry == "y":
            print("not available")#Not sure if i need that now tbh - Have to put it into sr manager prob
            raid_res_dict = raid_res_import.get_soft_reserve_players()
            attendeese_list = raid_attendance.get_raid_attendees()

            attended_players, not_attended_players = raid_attendance.intersect_raidres_and_attendees(attendeese_list,raid_res_dict)
            #print("-" * 20 + "Attended" + "-" * 20)
            #print_dictionary(attended_players)
            #print("-" * 20 + "Not Attended" + "-" * 20)
            #print_dictionary(not_attended_players)

            #read_write_csv.write_csv_file(attended_players)

            break
        
        elif user_entry == "n":
            print("Pls update >raidres.txt<")
            time.sleep(3)
            break
        else:
            print("Input not recognized")       

def print_dictionary(dictionary:dict):
    general_functions.print_menu_title("Player Dictionary")
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
                print(f"Player: {player}{" " * space}| Characters: {dictionary[player]}")
        else:
            print(f"Player: {player} | Characters: {dictionary[player]}")
    general_functions.print_line()

def mainloop():
    
    while True:
        general_functions.print_menu_title("Main Menu")
        for menu_opt in menu_options:
            print(menu_opt)
        general_functions.print_line()
        user_entry = input("Option: ")

        try:
            user_entry = int(user_entry)
            general_functions.print_line()

            if user_entry == 0:
                print("Quitting program...")
                read_write_csv.write_csv_file_players(player_dict)
                time.sleep(2)
                break
            elif user_entry == 1:
                print("not available")
                

            elif user_entry == 2:
                general_functions.print_line()
                print("[1] Add new player")
                print("[2] Add new characters")
                user_entry = input("Option: ")
                general_functions.print_line()
                if user_entry == "q":
                    continue
                elif user_entry == "1":
                    manage_dict_func.add_new_players(player_dict)

                elif user_entry == "2":
                    manage_dict_func.add_characters_to_player(player_dict)
                else:
                    print("invalid input")

            elif user_entry == 3:
                general_functions.print_line()
                print("[1] Delete player")
                print("[2] Delete character")
                user_entry = input("Option: ")
                general_functions.print_line()
                if user_entry == "q":
                    continue
                elif user_entry == "1":
                    manage_dict_func.delete_player(player_dict)
                    read_write_csv.write_csv_file_players(player_dict)

                elif user_entry == "2":
                    manage_dict_func.delete_character(player_dict)
                    read_write_csv.write_csv_file_players(player_dict)
                else:
                    print("invalid input")
            
            elif user_entry == 4:
                print_dictionary(player_dict)

            elif user_entry == 5:
                sr_sheet_manager.sheet_manager_start()

            else:
                pass

        except:
            print("invalid option")


print("Loading players...")
player_dict = read_write_csv.read_csv_file_players()

mainloop()