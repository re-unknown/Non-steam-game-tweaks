# add.py
import vdf
from tkinter import Tk, filedialog

def read_shortcuts_vdf(file_path):
    with open(file_path, 'rb') as file:
        data = file.read()
    shortcuts = vdf.binary_loads(data)
    return shortcuts

def write_shortcuts_vdf(file_path, shortcuts):
    with open(file_path, 'wb') as file:
        file.write(vdf.binary_dumps(shortcuts))

def add_shortcut(shortcuts, app_data):
    if 'shortcuts' not in shortcuts:
        shortcuts['shortcuts'] = {}
    new_app_id = str(len(shortcuts['shortcuts']))
    shortcuts['shortcuts'][new_app_id] = app_data
    return new_app_id

def select_exe_file():
    root = Tk()
    root.withdraw()  # Tkinterウィンドウを非表示にする
    file_path = filedialog.askopenfilename(filetypes=[("Executable files", "*.exe")])
    root.destroy()
    return file_path
