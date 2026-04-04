import gspread
import scripts.general_functions as gen_func
import os, time

alphabet = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]

def check_age_of_file() -> bool:
    if os.path.exists("./Data/_user/authorized_user.json"):
        time_file = os.path.getmtime("./Data/_user/authorized_user.json")
        rightnow = time.time()
        return 7 < ((rightnow - time_file)/86400)
    else:
        return False

def gspread_overwrite(link:str,row_data:list,start_cell:str = 'A1',worksheet_num:int = 0) -> bool:
    try:
        #Auto check if authorized user file is to old and needs to be refreshed.
        if check_age_of_file():
            os.remove('./Data/_user/authorized_user.json')
        gc = gspread.oauth(authorized_user_filename='./Data/_user/authorized_user.json')
    except:
        print('Google Connection Error')
    else:
        try:
            sh = gc.open_by_url(f'{link}')
        except:
            print('Google Link broken')
        else:
            try:
                worksheet = sh.get_worksheet(worksheet_num)
            except:
                print('Google Worksheet out of range')
            else:
                data_no_nothing = []
                for row in row_data:
                    if row[1].lower() == 'nothing':
                        pass
                    else:
                        data_no_nothing.append(row)
                
                end_col_row = calc_sheet_length(data_no_nothing,start_cell)

                worksheet.batch_clear([f"A{start_cell[1]}:X100"])
                #worksheet.format("A1:B1",{"backgroundColor":{"red":0.0,"green":1.0,"blue":0.5}})
                worksheet.update(data_no_nothing, f'{start_cell}:{end_col_row}')
                return True
    return False

def calc_sheet_length( sr_sheet:list, start_cell:str = 'A1'):
    start_cell_column = start_cell[0].lower()
    start_cell_row = int(start_cell[1])

    list_length = 10

    to_column = alphabet.index(start_cell_column)+list_length
    to_row = len(sr_sheet) + start_cell_row -1
    end_row_col = f'{alphabet[to_column].capitalize()}{to_row}'

    return end_row_col

def format_row_data(sr_sheet:list) -> list:
    
    edited_sr_sheet = []
    days_start = 7
    if len(sr_sheet[0]) >= 14:
        days_start = -6
    header_row = [sr_sheet[0][1],sr_sheet[0][3],sr_sheet[0][2],sr_sheet[0][5]]
    header_row.extend(sr_sheet[0][days_start:])
    
    edited_sr_sheet.append(header_row)
    for row in sr_sheet[1:]:
        new_row =[]
        new_row.extend([row[1],row[3],row[2],int(row[5])])
        new_row.extend(row[days_start:])
        edited_sr_sheet.append(new_row)
    return edited_sr_sheet
        

def export_to_gsheet(sr_plus_sheet:list):
    sr_plus_sheet = format_row_data(sr_plus_sheet)
    success = False
    entered_url = input('GSheet URL: ')
    try:
        entered_worksheet = int(input('Worksheet num(1,2,...): ')) - 1
        if entered_worksheet < 0:
            entered_worksheet = 0
    except ValueError:
        print("Error: Input can't be converted to int")
    except:
        print('Error: Worksheet input')
    else:
        entered_starting_cell = input('Starting Cell (Header:Player -> etc) like "A1": ')
        success = gspread_overwrite(entered_url,sr_plus_sheet,entered_starting_cell,entered_worksheet)

    if success:
        print(gen_func.color_text('successfully exported','gr'))
    else:
        print(gen_func.color_text('export failed','rd'))

def get_gsheet_data(link:str,worksheet:int,cells:str) -> list:
    try:
        #Auto check if authorized user file is to old and needs to be refreshed.
        if check_age_of_file():
            os.remove('./Data/_user/authorized_user.json')
        gc = gspread.oauth(authorized_user_filename='./Data/_user/authorized_user.json')
    except:
        print('Google Connection Error')
    else:
        sh = gc.open_by_url(link)
        worksheet = sh.get_worksheet(worksheet)
        data = worksheet.get(cells)
        return data
