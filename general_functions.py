from datetime import datetime

line_length = 50

def print_line(line_length = 50):
    print("-" * line_length)

def print_menu_title(title):
    max_length = line_length - len(title)
    left_line = max_length // 2
    right_line = max_length - left_line
    print("-" * left_line + title + right_line * "-")

def print_loaded_file(filename):
    message = "Loaded: "
    max_length = line_length - len(filename) - len(message)
    print("-" * max_length + message + filename)

def get_user_input(question:str):
    user_input = input(f"{question}: ")
    return user_input

def get_date() -> str:
    date = str(datetime.now().strftime('%Y-%m-%d'))
    return date