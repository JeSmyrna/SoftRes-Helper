def intersect_raidres_and_attendees(attendeese:list, raidres:dict) -> tuple[dict,dict]:
    attendees_dict = {}
    not_attended_dict = {}

    for player in raidres:
        items = []

        if player in attendeese:
            items = raidres.get(player)
            if items == []:
                print(f'no raidres found for {player}')
                items = 'Nothing'
            
            attendees_dict.update({player:items})
        else:
            not_attended_dict.update({player:items})

    return attendees_dict,not_attended_dict