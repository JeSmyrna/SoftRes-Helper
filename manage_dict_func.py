import time
import general_functions

#go through character name check for valid characters in name
valid_characters = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
def check_if_name_valid(playername: str):
    playername = playername.lower()
    for char in playername:
        if char not in valid_characters:
            return False
    return True

#function to make the character list and pack it into a string format
def combine_character_names(character_names: list) -> str:
    name_string = ""
    if len(character_names) > 1:
        for name in character_names:
            name_string += name + "."
        return name_string[:-1]
    else:
        name_string = str(character_names[0])
        return name_string

#add new players to dictionary, looping till user ends the loop with key - "q"
def add_new_players(player_dict:dict):
    while True:
        user_entry_playername = input("new player: ")
        if user_entry_playername == "q":
            print("stop editing...")
            time.sleep(1)
            break

        #Make sure player is unique and doesnt already exist
        elif check_if_player_exists(user_entry_playername,player_dict):
            print("Player already exists")
            time.sleep(0.5)
            
            user_entry = input(f"add characters to {user_entry_playername}? (y/n): ")
            if user_entry == "y":
                add_characters_to_player(player_dict,user_entry_playername)
            elif user_entry == "n":
                print("choose different player...")
                time.sleep(0.5)
            else:
                print("invalid input")

        #If new, continue
        else:
            character_list = []
            while True:
                user_entry_character = input("Character?: ")
                if user_entry_character == "q":
                    break
                else:
                    if check_if_name_valid(user_entry_character):
                        character_list.append(user_entry_character)
                        print(character_list)
                    else:
                        print("Not a valid name")
                        
            player_dict[user_entry_playername] = combine_character_names(character_list)

def find_player(player_dict):
    while True:
        playername = input("Player: ")
        if playername == "q":
            return "", []
        
        elif playername in player_dict:
            characters = str(player_dict[playername]).split(".")
            return playername, characters
            
        else:
            print("player not found")

def add_characters_to_player(player_dict, playername = ''):
    if playername == "":
        playername, characters = find_player(player_dict)
        if playername == "" or characters == []:
            return
    else:
        characters = str(player_dict[playername]).split(".")
    
    print_player_and_characters(playername, characters)

    while True:
        user_entry_character = input("New Character: ")
        if user_entry_character == "q":
            break
        else:
            if check_if_name_valid(user_entry_character):
                characters.append(user_entry_character)
                print_player_and_characters(playername, characters)
            else:
                print("Not a valid name")
                
    player_dict[playername] = combine_character_names(characters)

##Visualising Player and their characters
def print_player_and_characters(playername, characters):
    player_characters = ""
    for name in characters:
        player_characters += name + " - "
    player_characters = player_characters[:-3]

    space = 16 - len(playername)
    general_functions.print_line()
    print(f"Player: {playername}{" " * space}| Characters: {player_characters}")
    general_functions.print_line()
def delete_character(player_dict):
    
    playername, characters = find_player(player_dict)

    while True:
        print_player_and_characters(playername, characters)
        user_input = input("Delete Character: ")
        if user_input == "q":
            player_dict[playername] = combine_character_names(characters)
            return
        elif user_input in characters:
            characters.remove(user_input)
        else:
            print("invalid input")


#test_dict = {"player" : "player1.player2.player3"}
#delete_character(test_dict)
#add_characters_to_player("player",test_dict)

def delete_player(player_dict:dict):
    while True:
        user_entry_playername = input("Delete player: ")
        if user_entry_playername == "q":
            print("back to menu...")
            time.sleep(2)
            break
        #make sure player exists in dictionary before deleting
        elif not check_if_player_exists(user_entry_playername,player_dict):
            print("Player doesn't exist..")
            time.sleep(1)
        else:    
            print(f"Player: {user_entry_playername} | Characters: {player_dict[user_entry_playername]}")
            entry_make_sure = input(f'Delete player "{user_entry_playername}"? (y/n): ')
            
            if entry_make_sure == "y":
                print(f"Deleting player {user_entry_playername} ...")
                player_dict.pop(user_entry_playername)
                time.sleep(1)
            elif entry_make_sure == "n":
                pass
            
            else:
                print("invalid input")

#Checking if key already exists in dictionary
def check_if_player_exists(playername: str, player_dict: dict) -> bool:
    if playername in player_dict:
        return True
    else:
        return False