import gspread
import read_write_csv as rw_csv

alphabet = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]

def gspread_overwrite(link:str,row_data:dict):
    gc = gspread.oauth()
    sh = gc.open_by_url(f'{link}')
    row = len(row_data)
    worksheet = sh.get_worksheet(0)

    list_length = len(row_data['columns']) - 1
    lists = []

    for entry in row_data:
        lists.append(row_data[entry])

    worksheet.update(lists, f'A1:{alphabet[list_length].capitalize()}{row}')

def load_sr_sheet_data(filename:str):
    data = rw_csv.load_sr_sheet(f'{filename}')
        
    return data
