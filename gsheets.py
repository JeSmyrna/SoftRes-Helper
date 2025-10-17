import gspread
import general_functions as gen_func

alphabet = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]

def gspread_overwrite(link:str,row_data:dict,start_cell:str = 'A1',worksheet_num:int = 0) -> bool:
    try:
        gc = gspread.oauth()
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
                data_no_nothing = {}
                for row in row_data:
                    if row_data[row][1] == 'Nothing':
                        pass
                    elif '-' in row_data[row][1]:
                        row_data[row][1] = str(row_data[row][1]).replace(' - ',', ')
                        
                        data_no_nothing.update({row:row_data[row]})
                    else:
                        data_no_nothing.update({row:row_data[row]})
                
                end_col_row = calc_sheet_length(data_no_nothing,start_cell)
                lists = []
                for entry in data_no_nothing:
                    #ignore player who have no SR+
                    lists.append(row_data[entry])

                worksheet.batch_clear([f"A{start_cell[1]}:L50"])
                worksheet.update(lists, f'{start_cell}:{end_col_row}')
                return True
    return False

def calc_sheet_length( sr_sheet:dict, start_cell:str = 'A1'):
    start_cell_column = start_cell[0].lower()
    start_cell_row = int(start_cell[1])

    list_length = len(sr_sheet['columns'])-1

    to_column = alphabet.index(start_cell_column)+list_length
    to_row = len(sr_sheet) + start_cell_row -1
    end_row_col = f'{alphabet[to_column].capitalize()}{to_row}'

    return end_row_col

def export_to_gsheet(sr_plus_sheet:dict):
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