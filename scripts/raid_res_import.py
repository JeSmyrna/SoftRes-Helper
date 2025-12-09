import scripts.read_write_csv as rw_csv

raid_res_player_dict = {}

def format_sr_players(user_entry):
    player_list = user_entry.split(": ")
    player_list.pop(0)
    player_list = [': '.join(player_list)]
    player_item = str(player_list[0]).split(" - ")
    if len(player_item) > 2:
        formula_name = player_item[1] + ' - ' + player_item[2]
        player_name = player_item[0]
        player_item.clear()
        player_item = [player_name,formula_name]
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

def get_players_sr_and_comments(filename="raidres"):
    raidres_list = rw_csv.load_raidres(f'Import/{filename}')
    raid_res_player_dict = {}

    #make key list
    keys = [attendee[1] for attendee in raidres_list if attendee[1] != 'Attendee']
    keys.sort()
    for key in keys:
        items = []
        comments = []
        for item in raidres_list:
            if key == item[1]:
                items.append(item[0])
                comments.append(item[2])
        """ if len(items) == 1:
            items.append(items[0])
            comments.append('') """
        items.extend(comments)
        raid_res_player_dict.update({key:items})
    return raid_res_player_dict


#raid_res_player_dict = get_players_sr_and_comments()
#for entry in raid_res_player_dict:
#    print(f"{entry} : {raid_res_player_dict[entry]}")

