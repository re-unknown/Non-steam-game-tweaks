import flet as ft
import random
import os
import requests
from tkinter import Tk, filedialog
from steamgriddb import search_game, get_grids_by_gameid
from add import add_shortcut
from remove import read_shortcuts_vdf, write_shortcuts_vdf
from image_selection_window import open_image_selection_window

def select_exe_file():
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    file_path = filedialog.askopenfilename(filetypes=[("Executable files", "*.exe")])
    root.destroy()
    return file_path

def close_dialog(dialog, page):
    dialog.open = False
    page.update()

def show_add_shortcut_dialog(page, file_path, shortcuts, main):
    app_id = f"-{random.randint(1000000000, 9999999999)}"  # appidを決定
    app_id_number = app_id.lstrip('-')  # マイナスを抜いた数値
    selected_image_url = None

    def set_selected_image_url(url):
        nonlocal selected_image_url
        selected_image_url = url

    def add_shortcut_action(e):
        exe_path = exe_input.value.replace('/', '\\')
        app_data = {
            'appid': app_id,
            'AppName': appname_input.value,
            'Exe': f'"{exe_path}"',
            'StartDir': startdir_input.value.replace('/', '\\')
        }
        add_shortcut(shortcuts, app_data)
        write_shortcuts_vdf(file_path, shortcuts)
        if selected_image_url:
            save_image(selected_image_url, app_id_number, file_path)
        close_dialog(dialog, page)
        page.controls.clear()
        main(page)

    def save_image(url, app_id_number, file_path):
        response = requests.get(url)
        if response.status_code == 200:
            grid_folder = os.path.join(os.path.dirname(file_path), 'grid')
            os.makedirs(grid_folder, exist_ok=True)
            image_path = os.path.join(grid_folder, f"{app_id_number}.jpg")
            with open(image_path, 'wb') as file:
                file.write(response.content)

    def select_exe(e):
        exe_path = select_exe_file()
        if exe_path:
            exe_input.value = exe_path.replace('/', '\\')
            startdir_input.value = os.path.dirname(exe_path).replace('/', '\\') + "\\"
            page.update()

    appname_input = ft.TextField(label="App Name")
    exe_input = ft.TextField(label="Exe", expand=True)
    exe_button = ft.ElevatedButton("Browse", on_click=select_exe)
    startdir_input = ft.TextField(label="Start Dir")
    app_id_text = ft.Text(f"App ID: {app_id}")  # appidを表示
    image_button = ft.ElevatedButton("Select Image", on_click=lambda e: open_image_selection_window(page, dialog, set_selected_image_url))

    dialog = ft.AlertDialog(
        title=ft.Text("Add Shortcut"),
        content=ft.Column([
            app_id_text,  # appidを表示
            appname_input,
            ft.Row([exe_input, exe_button], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            startdir_input,
            image_button
        ]),
        actions=[
            ft.TextButton("Add", on_click=add_shortcut_action),
            ft.TextButton("Cancel", on_click=lambda e: close_dialog(dialog, page))
        ]
    )
    page.overlay.append(dialog)
    dialog.open = True
    page.update()
