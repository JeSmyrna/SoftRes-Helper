import time
import general_functions
import read_write_csv
import sr_sheet_manager_func

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
sr_sheets = []

menu_option = [
    "[0] return to main menu",
    "[1] load raid sheet", #choose what sheet to load
    "[2] create new raid SR+ sheet", # create a new SR+ sheet with choosen name, maybe people manage multiple guilds SR sheets so get the name ""
    "[3] print SR+ Sheet"
]
def load_sr_sheet(filename) -> dict:
    if filename == "[Empty]":
        return filename
    
    else:
        print("loading file...")
        file = read_write_csv.load_sr_sheet(filename)
        #load csv raid file
        
        time.sleep(1)
        if file == {}:
            #print(filename, file)
            return file, "[Empty]"
        else:
            #print(filename, file)
            return file, filename
        #general_functions.print_loaded_file(filename)


def print_available_sheets(raid_sheets):
    for sheet in raid_sheets:
        print(sheet)
        time.sleep(.15)
    general_functions.print_line()



def choose_sheet():
    sr_sheets = read_write_csv.load_sr_sheets_directory()
    print_available_sheets(sr_sheets)
    user_input = input("Choose Sheet: ")
    file, filename = load_sr_sheet(user_input)
    sheet_manager_start(file, filename)



def sheet_manager_start(sheet = {}, sheet_name = "[Empty]"): #get player dictionary ?
    general_functions.print_menu_title("SR Sheet Manager")
    
    #in case of coming back from editing a sheet, sheet is already loaded so don't show the available ones
    if sheet != {}:
        general_functions.print_loaded_file(sheet_name)
        sheet_manager_main(sheet,sheet_name)
    
    #catch if no sheet is loaded
    else:
        general_functions.print_loaded_file(load_sr_sheet(sheet_name))
        choose_sheet()
    

def sheet_manager_main(raid_sheet,filename):
    while True:
        #show menu options, List at the top
        for option in menu_option:
            print(option)

        user_input = input("Choose: ")
        if user_input == "0":
            time.sleep(1)
            return
        
        elif user_input == "1":
            pass
        elif user_input == "2":
            pass
        elif user_input == "3":
            general_functions.print_menu_title(filename)
            sr_sheet_manager_func.print_sr_plus_sheet(raid_sheet)
        else:
            print("invalid input")

sheet_manager_start()