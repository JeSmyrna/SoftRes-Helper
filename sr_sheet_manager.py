import time
import general_functions
import read_write_csv
import sr_sheet_manager_func

sr_plus_dict = {}
sr_plus_dict_archive = {}


#Testing file
sr_sheets = []

menu_option = [
    "[0] return to main menu",
    "[1] load raid sheet", #choose what sheet to load
    "[2] create new raid SR+ sheet", # create a new SR+ sheet with choosen name, maybe people manage multiple guilds SR sheets so get the name ""
    "[3] print SR+ Sheet",
    "[4] save SR+ Sheet",
    "[5] make new entry",
    "[6] add player to sheet",
    "[7] Player SR+ aquired"
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
    
    #in case of coming back from editing a sheet, sheet is already loaded so don't show the available ones
    if sheet != {}:
        sheet_manager_main(sheet,sheet_name)
    
    #catch if no sheet is loaded
    else:
        general_functions.print_loaded_file(load_sr_sheet(sheet_name))
        choose_sheet()
    

def sheet_manager_main(raid_sheet,filename):
    file_edited = False

    while True:
        general_functions.print_menu_title("SR Sheet Manager")
        general_functions.print_loaded_file(filename)
        #show menu options, List at the top
        for option in menu_option:
            print(option)
            time.sleep(0.1)

        general_functions.print_line()
        user_input = input("Choose: ")
        if user_input == "0":
            time.sleep(1)
            return
        
        #load SR Sheet
        elif user_input == "1":
            break

        #create SR sheet
        elif user_input == "2":
            sr_sheet_manager_func.create_new_sr_plus_sheet()
            time.sleep(1)
            print_available_sheets(read_write_csv.load_sr_sheets_directory())

        #print SR sheet
        elif user_input == "3":
            general_functions.print_menu_title(filename)
            time.sleep(0.5)
            sr_sheet_manager_func.print_sr_plus_sheet(raid_sheet)
            time.sleep(0.5)
        
        #save SR sheet
        elif user_input == "4":
            print("saving file...")
            read_write_csv.safe_sr_sheet_csv(filename,raid_sheet)
            print("file is safed")
            general_functions.print_line()
            time.sleep(1)
        
        #make new entry in SR sheet
        elif user_input == "5":
            general_functions.print_menu_title(f"New Entry to {filename}")
            raid_sheet = sr_sheet_manager_func.make_new_entry(filename,raid_sheet)
            general_functions.print_line()

        elif user_input == "6":
            sr_sheet_manager_func.add_players_manual_to_sheet(filename,raid_sheet)
            general_functions.print_line()
            file_edited = True
            break
        elif user_input == "7":
            sr_sheet_manager_func.award_sr_plus(filename,raid_sheet)
            general_functions.print_line()
            file_edited = True
            break
        else:
            print("invalid input")

    #loop break to choose different sheet
    if file_edited: #Auto select current edited file
        file, filename = load_sr_sheet(filename)
        sheet_manager_start(file, filename)
    else:
        sheet_manager_start()