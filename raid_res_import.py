import time

raid_res_player_dict = {}

def format_sr_players(user_entry):
    
    player_list = user_entry.split("[00:00]")
    player_list.pop(0)
    for player in player_list:
        first_part = player.split(":")
        secnd_part = first_part[1].split(" - ")
        item = secnd_part[1]
        item = item[:-1]
        if first_part[0] not in raid_res_player_dict:
            raid_res_player_dict[first_part[0]] = item
        else:
            raid_res_player_dict[first_part[0]] += "," + item
                        
    

def get_soft_reserve_players():
    with open("raidres.txt") as file_in:
        lines = []
        for line in file_in:
            lines.append(line)
        
        for entry in lines:
            format_sr_players(entry)

    return raid_res_player_dict

        #for entry in raid_res_player_dict:
            #print(f"{entry} : {raid_res_player_dict[entry]}")