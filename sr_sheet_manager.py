import time
import general_functions

sr_plus_dict = {}
sr_plus_dict_archive = {}

# SR Sheet IteraitingNumber + Raidname / + Archive
# functions: load sr sheet active, ask which raid > show available raids
# loading: columns in list so we can fill new players columns with empty
# if sum(if not empty/"-" > of attended dates += 1) * 10
# No available or need more/new raid SR > create new SR raid + archive doc
# add new player and SR to active sheet
# new player > fill already entered columns with "-"
# check attendance
# check attendance sr in sr sheet, add bonus roll if same sr was made
# if SR is not the same, SR+ was changed and with that reset bonusroll
# put into archive when changed

# Archive
# check if player got sr+ item, if yes > put into archive {1: [Player, item, Bonusroll, status (aquired or changed), status date, dates attendance]}

#Testing file
testing_dict = [{"filename": "Stonewall Inn BWL"},
                {"filename": "Stonewall Inn AQ40"},
                {"filename" : "Stonewall Inn ES"}]



menu_option = [
    "[0] return to main menu",
    "[1] load raid sheet", #choose what sheet to load
    "[2] create new raid SR+ sheet", # create a new SR+ sheet with choosen name, maybe people manage multiple guilds SR sheets so get the name ""
    "[3] "
]
def load_sr_sheet(filename = "[Empty]") -> dict:
    if filename == "[Empty]":
        return filename
    
    for file in testing_dict:
        if filename == file["filename"]:
            print("loading file...")
            time.sleep(1)
            return file
        #general_functions.print_loaded_file(filename)


def print_available_sheets(raid_sheets):
    for sheet in raid_sheets:
        print(sheet["filename"])
        time.sleep(.15)
    general_functions.print_line()

def choose_sheet():
    print_available_sheets(testing_dict)
    user_input = input("Choose Sheet: ")
    sheet_manager_start(load_sr_sheet(user_input))

def sheet_manager_start(sheet_dict = {}): #get player dictionary ?
    general_functions.print_menu_title("SR Sheet Manager")
    
    #in case of coming back from editing a sheet, sheet is already loaded so don't show the available ones
    if sheet_dict != {}:
        general_functions.print_loaded_file(sheet_dict["filename"])
        sheet_manager_main(sheet_dict)
    
    #catch if no sheet is loaded
    else:
        general_functions.print_loaded_file(load_sr_sheet())
        choose_sheet()
    

def sheet_manager_main(sheet_dict):
    while True:
        #show menu options, List at the top
        for option in menu_option:
            print(option)

        user_input = input("Choose: ")
        if user_input == "0":
            time.sleep(1)
            return
        else:
            print("invalid input")

#sheet_manager_start()