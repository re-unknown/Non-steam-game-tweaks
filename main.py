import flet as ft
from remove import read_shortcuts_vdf, delete_shortcut, write_shortcuts_vdf, compact_app_ids, delete_app, close_dialog
from add import add_shortcut, select_exe_file
import os
import random
from tkinter import Tk, filedialog
from steamgriddb import search_game, get_grids_by_gameid
from show_add_shortcut_dialog import show_add_shortcut_dialog

def select_exe_file():
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    file_path = filedialog.askopenfilename(filetypes=[("Executable files", "*.exe")])
    root.destroy()
    return file_path

def find_shortcuts_vdf():
    steam_path = os.path.expandvars(r'%ProgramFiles(x86)%\Steam\userdata')
    for root, _, files in os.walk(steam_path):
        if 'shortcuts.vdf' in files:
            return os.path.join(root, 'shortcuts.vdf')
    return None

def main(page: ft.Page):
    page.title = "Steam add app tweaks"

    file_path = find_shortcuts_vdf()
    if not file_path:
        print("shortcuts.vdfが見つかりませんでした。")
        return

    shortcuts = read_shortcuts_vdf(file_path)
    shortcuts.setdefault('shortcuts', {})

    path_text = ft.Text(f"shortcuts.vdfのパス: {file_path}")
    page.controls.append(path_text)

    scroll_container = ft.Column(scroll=ft.ScrollMode.AUTO)
    page.controls.append(scroll_container)

    def update_layout(e):
        card_width = page.window.width / 2 - 20
        scroll_container.height = page.window.height - 80
        for row in scroll_container.controls:
            for card in row.controls:
                card.width = card_width
        page.update()

    page.on_resized = update_layout

    row = ft.Row()
    scroll_container.controls.append(row)

    for app_id, app_data in shortcuts['shortcuts'].items():
        card = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text(f"App ID: {app_id}"),
                    ft.Text(f"appid: {app_data.get('appid', 'N/A')}, AppName: {app_data.get('AppName', 'N/A')}"),
                    ft.Text(f"Exe: {app_data.get('Exe', 'N/A')}"),
                    ft.Text(f"StartDir: {app_data.get('StartDir', 'N/A')}"),
                    ft.Text(f"tags: {app_data.get('tags', 'N/A')}"),
                    ft.ElevatedButton("Delete", on_click=lambda e, app_id=app_id: delete_app(page, file_path, app_id, main))
                ]),
                padding=10
            )
        )
        row.controls.append(card)
        if len(row.controls) == 2:
            row = ft.Row()
            scroll_container.controls.append(row)

    current_page = 0
    images_per_page = 10
    global all_images
    all_images = []

    add_button = ft.FloatingActionButton(icon=ft.icons.ADD, on_click=lambda e: show_add_shortcut_dialog(page, file_path, shortcuts, main))
    page.controls.append(add_button)

    update_layout(None)
    page.update()

ft.app(target=main)
