import time

def add_new_players(player_dict:dict):
    while True:
        user_entry_playername = input("new player: ")
        if user_entry_playername == "q":
            print("stop editing...")
            time.sleep(1)
            break
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
            

def combine_character_names(character_names: list) -> str:
    name_string = ""
    if len(character_names) > 1:
        for name in character_names:
            name_string += name + "."
        return name_string[:-1]
    else:
        return name_string


valid_characters = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
def check_if_name_valid(playername: str):
    playername = playername.lower()
    for char in playername:
        if char not in valid_characters:
            return False
    return True

#test_list = ["Bern", "Peter", "warze"]
#print(combine_character_names(test_list))