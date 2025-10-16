import time
import general_functions
import read_write_csv
import sr_sheet_manager_func
import gsheets

sr_plus_dict = {}
sr_plus_dict_archive = {}


#Testing file
sr_sheets = []

menu_option = [
    "[0] return to main menu",
    "",
    "[1] load raid sheet", #choose what sheet to load
    "[2] create new raid SR+ sheet", # create a new SR+ sheet with choosen name, maybe people manage multiple guilds SR sheets so get the name ""
    "[3] print SR+ Sheet",
    "[4] export to gsheet",
    "",
    "[5] make new entry",
    "",
    "--- manual changes ---",
    "[6] Delete Player SR+",
    "[7] add player to sheet",
    "[8] Award Player SR+",
    "[9] Award SR+ with loot log"
    
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
    index = 0
    for sheet in raid_sheets:
        index += 1
        print(f'[{index}] - {sheet}')
        time.sleep(.15)
    general_functions.print_line()



def choose_sheet():
    sr_sheets = read_write_csv.load_sr_sheets_directory()
    print_available_sheets(sr_sheets)
    while True:
        user_input = input("Choose Sheet: ")#choose by number not by string name
        try:
            index = int(user_input) -1
            if 0 <= index < len(sr_sheets):
                break  
            else:
                print(f'sheet {user_input} not available')
                general_functions.print_line(20)
                pass
        except:
            print("invald input...")
    file, filename = load_sr_sheet(sr_sheets[index])
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
            raid_sheet = sr_sheet_manager_func.print_sr_plus_sheet(raid_sheet)
            read_write_csv.safe_sr_sheet_csv(filename,raid_sheet)
            time.sleep(0.5)
        
        #save SR sheet
        #elif user_input == "4": "[4] save SR+ Sheet"
            #print("saving file...")
            #read_write_csv.safe_sr_sheet_csv(filename,raid_sheet)
            #print("file is safed")
            #general_functions.print_line()
            #time.sleep(1)
        elif user_input == '4':
            general_functions.print_line()
            ask_user_export = input(f'Export current sheet {general_functions.color_text(filename,'yw')} to gsheets? (y/n): ')
            if ask_user_export == 'y':
                general_functions.print_line(20)
                print('exporting file to gsheets...')
                gsheets.export_to_gsheet(raid_sheet)
                print('successfully exported')
                time.sleep(1)
            else:
                print('canceling export...')
                time.sleep(1)
                pass
            general_functions.print_line()
        
        #make new entry in SR sheet
        elif user_input == "5":
            general_functions.print_menu_title(f"New Entry to {filename}")
            raid_sheet = sr_sheet_manager_func.make_entry(filename,raid_sheet)
            general_functions.print_line()

        
        elif user_input == "6":
            sr_sheet_manager_func.delete_player_manually_from_sheet(filename,raid_sheet)
            general_functions.print_line()
            file_edited = True
            break
        elif user_input == "7":
            sr_sheet_manager_func.add_players_manual_to_sheet(filename,raid_sheet)
            general_functions.print_line()
            file_edited = True
            break
        elif user_input == "8":
            sr_sheet_manager_func.award_sr_plus(filename,raid_sheet)
            general_functions.print_line()
            file_edited = True
            break
        elif user_input == "9":
            sr_sheet_manager_func.award_through_loot_log(filename,raid_sheet)
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