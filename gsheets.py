import gspread
import read_write_csv as rw_csv

alphabet = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]

def gspread_overwrite(link:str,row_data:dict,start_cell:str = 'A1'):
    gc = gspread.oauth()
    sh = gc.open_by_url(f'{link}')
    worksheet = sh.get_worksheet(1)
    data_no_nothing = {}
    for row in row_data:
        if row_data[row][1] == 'Nothing':
            pass
        else:
            data_no_nothing.update({row:row_data[row]})
    
    end_col_row = calc_sheet_length(data_no_nothing,start_cell)
    lists = []
    for entry in data_no_nothing:
        #ignore player who have no SR+
        lists.append(row_data[entry])

    worksheet.batch_clear([f"A{start_cell[1]}:A50",f"B{start_cell[1]}:B50",f"C{start_cell[1]}:C50",f"D{start_cell[1]}:D50",f"E{start_cell[1]}:E50",f"F{start_cell[1]}:F50", f"G{start_cell[1]}:G50", f"H{start_cell[1]}:H50", f"I{start_cell[1]}:I50", f"J{start_cell[1]}:J50", f"K{start_cell[1]}:K50", f"L{start_cell[1]}:L50"])
    worksheet.update(lists, f'{start_cell}:{end_col_row}')

def calc_sheet_length( sr_sheet:dict, start_cell:str = 'A1'):
    start_cell_column = start_cell[0].lower()
    start_cell_row = int(start_cell[1])

    list_length = len(sr_sheet['columns'])-1

    to_column = alphabet.index(start_cell_column)+list_length
    to_row = len(sr_sheet) + start_cell_row -1
    end_row_col = f'{alphabet[to_column].capitalize()}{to_row}'

    return end_row_col

def export_to_gsheet(sr_plus_sheet):
    entered_url = input('GSheet URL: ')
    entered_starting_cell = input('Starting Cell (Header:Player -> etc) like "A1": ')
    gspread_overwrite(entered_url,sr_plus_sheet,entered_starting_cell)