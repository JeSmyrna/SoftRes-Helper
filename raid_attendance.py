
def get_raid_attendees():
    attendees_list = []

    with open("attendeese.txt") as file_in:
        for line in file_in:
            attendees_list.append(line.rstrip("\n"))

    return attendees_list

def intersect_raidres_and_attendees(attendeese:list, raidres:dict):
    attendees_dict = {}
    not_attended_dict = {}
    for player in raidres:
        if player in attendeese:
            attendees_dict[player] = raidres[player]
        else:
            not_attended_dict[player] = raidres[player]

    return attendees_dict,not_attended_dict

