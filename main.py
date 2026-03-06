from scripts.player_mng import PlayerManager

from scripts.general_functions import print_menu_title
from time import sleep

menu_options = [
    "[0] Quit program",
    "[1] add more players or characters",
    "[2] delete player or characters",
    "[3] print dict",
    "[4] Manage SR+ Sheet"
                ]

timer = 1

def main():
    player_mng = PlayerManager()
    while True:
        print(chr(27) + "[2J") #clear terminal
        print_menu_title("Main Menu")
        for option in menu_options:
            print(option)

        print("-"*20)
        user_input = input("Option: ")

        if user_input == "0":
            print("closing programm...")
            sleep(timer)
            return
        elif user_input == "1":
            while True:
                print(chr(27) + "[2J") #clear terminal
                print_menu_title("Add Character")
                print("[0] Go back")
                ask_name = input("name: ").capitalize()
                if ask_name == "0":
                    print("going back...")
                    sleep(timer)
                    break

                if player_mng._ask_user(f"Is {ask_name} an alt?"):
                    player_mng.print_chars()
                    ask_owner = input("owner: ").capitalize()
                else:
                    ask_owner = ask_name
                print("-"*20)
                ask_class = player_mng.choose_class()

                if ask_class == False:
                    print("canceling...")
                    sleep(timer)
                    break
                if player_mng._ask_user(f"Want to add {ask_name} | {ask_class} | {ask_owner}"):
                    player_mng.add_player({"name":ask_name,"class":ask_class,"owner":ask_owner})
                    sleep(timer)
                else:
                    break
        elif user_input == "2":
            while True:
                print(chr(27) + "[2J") #clear terminal
                print_menu_title("Delete Char or Player")
                ask_user = input("""[0] going back
                                 
[1] delete Character
[2] delete Player
option: """)
                if ask_user == "0":
                    print("going back...")
                    sleep(timer)
                    break
                #print(chr(27) + "[2J") #clear terminal
                player_mng.print_chars()
                
                if ask_user == "1":
                    ask_name = input("Delete character: ").capitalize()
                    player_mng.delete_player(ask_name)
                    
                elif ask_user == "2":
                    ask_name = input("Delete all characters of player: ").capitalize()
                    player_mng.delete_player(ask_name,True)
                else:
                    print("not an option")
                sleep(timer)

        elif user_input == "3":
            print(" ")
            player_mng.print_chars()
            input("press enter to continue ...")
main()