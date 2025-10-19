import scripts.read_write_csv as read_write_csv
import scripts.manage_dict_func as manage_dict_func
import scripts.sr_sheet_manager as sr_sheet_manager
import scripts.general_functions as general_functions
import time



menu_options = [
    "[0] Quit program",
    "[1] add more players or characters",
    "[2] delete player or characters",
    "[3] print dict",
    "[4] Manage SR+ Sheet"
                ]

player_dict = {}  

def mainloop():

    print("Loading players...")
    player_dict = general_functions.order_dict_alphabetically(read_write_csv.read_csv_file_players())
    
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
                manage_dict_func.print_dictionary(player_dict)
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

                player_dict = general_functions.order_dict_alphabetically(player_dict)
                read_write_csv.write_csv_file_players(player_dict)

            elif user_entry == 2:
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
                    
                player_dict = general_functions.order_dict_alphabetically(player_dict)
                read_write_csv.write_csv_file_players(player_dict)
            
            elif user_entry == 3:
                #player_dict = read_write_csv.read_csv_file_players()
                manage_dict_func.print_dictionary(player_dict)

            elif user_entry == 4:
                sr_sheet_manager.sheet_manager_start()

            else:
                pass

        except:
            print("invalid option")


mainloop()