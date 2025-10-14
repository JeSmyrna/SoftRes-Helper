import time
import read_write_csv as rw_csv

raid_res_player_dict = {}

def format_sr_players(user_entry):
    player_list = user_entry.split(": ")
    player_list.pop(0)
    player_item = str(player_list[0]).split(" - ")
    return player_item 

def get_soft_reserve_players():
    with open("raidres.txt") as file_in:
        lines = []
        for line in file_in:
            lines.append(line.rstrip('\n'))
        
        for entry in lines:

            items = format_sr_players(entry)

            keys_in_dict = raid_res_player_dict.keys()

            if items[0] in keys_in_dict:
                char_items = raid_res_player_dict[items[0]]
                char_items.append(items[1])
                
                raid_res_player_dict[items[0]] = char_items
            else:
                raid_res_player_dict[items[0]] = [items[1]]

    return raid_res_player_dict

#for entry in raid_res_player_dict:
#    print(f"{entry} : {raid_res_player_dict[entry]}")

