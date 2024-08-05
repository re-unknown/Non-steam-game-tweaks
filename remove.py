import vdf
import flet as ft

def read_shortcuts_vdf(file_path):
    with open(file_path, 'rb') as file:
        data = file.read()
    shortcuts = vdf.binary_loads(data)
    return shortcuts

def write_shortcuts_vdf(file_path, shortcuts):
    with open(file_path, 'wb') as file:
        file.write(vdf.binary_dumps(shortcuts))

def delete_shortcut(shortcuts, app_id):
    if 'shortcuts' in shortcuts and app_id in shortcuts['shortcuts']:
        del shortcuts['shortcuts'][app_id]
        return True
    return False

def compact_app_ids(shortcuts):
    if 'shortcuts' in shortcuts:
        new_shortcuts = {'shortcuts': {}}
        new_app_id = 0
        for app_data in shortcuts['shortcuts'].values():
            new_shortcuts['shortcuts'][str(new_app_id)] = app_data
            new_app_id += 1
        return new_shortcuts
    return shortcuts

def print_shortcuts(shortcuts):
    if 'shortcuts' in shortcuts:
        for app_id, app_data in shortcuts['shortcuts'].items():
            print(f"App ID: {app_id}")
            for key, value in app_data.items():
                print(f"  {key}: {value}")
    else:
        print("No shortcuts found.")

def close_dialog(dialog, page):
    dialog.open = False
    page.update()

def delete_app(page, file_path, app_id, main):
    def confirm_delete(e):
        shortcuts = read_shortcuts_vdf(file_path)
        if delete_shortcut(shortcuts, app_id):
            shortcuts = compact_app_ids(shortcuts)
            write_shortcuts_vdf(file_path, shortcuts)
            page.controls.clear()
            main(page)
        dialog.open = False
        page.update()

    dialog = ft.AlertDialog(
        title=ft.Text("確認"),
        content=ft.Text("本当にこのアプリを削除しますか？"),
        actions=[
            ft.TextButton("キャンセル", on_click=lambda e: close_dialog(dialog, page)),
            ft.TextButton("削除", on_click=confirm_delete)
        ]
    )
    page.overlay.append(dialog)
    dialog.open = True
    page.update()
