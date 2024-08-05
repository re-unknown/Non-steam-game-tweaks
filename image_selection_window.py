import flet as ft
from steamgriddb import search_game, get_grids_by_gameid

def open_image_selection_window(page, previous_dialog, set_selected_image_url):
    current_page = 0
    images_per_page = 10
    global all_images
    all_images = []

    def select_image(e):
        app_name = search_input.value
        if app_name:
            results = search_game(app_name)
            if results:
                image_list.controls.clear()
                global all_images
                all_images = []
                for game in results:
                    game_id = game.id
                    grids = get_grids_by_gameid(game_id)
                    if grids:
                        for grid in grids:
                            image = ft.Container(
                                content=ft.Image(src=grid.url, width=100, height=100),
                                on_click=lambda e, url=grid.url: select_image_url(url)
                            )
                            all_images.append(image)
                show_images(0)

    def select_image_url(url):
        set_selected_image_url(url)
        close_dialog(image_selection_dialog, page, previous_dialog)

    def show_images(page_num):
        nonlocal current_page
        current_page = page_num
        start_index = page_num * images_per_page
        end_index = start_index + images_per_page
        image_list.controls.clear()
        row = ft.Row()
        for i, image in enumerate(all_images[start_index:end_index]):
            row.controls.append(image)
            if (i + 1) % 5 == 0:
                image_list.controls.append(row)
                row = ft.Row()
        if row.controls:
            image_list.controls.append(row)
        image_selection_dialog.update()

    def next_page(e):
        show_images(current_page + 1)

    def prev_page(e):
        show_images(current_page - 1)

    search_input = ft.TextField(label="App Name", on_submit=select_image)
    image_list = ft.Column()
    next_button = ft.ElevatedButton("Next", on_click=next_page)
    prev_button = ft.ElevatedButton("Previous", on_click=prev_page)

    image_selection_dialog = ft.AlertDialog(
        title=ft.Text("Select Image"),
        content=ft.Column([
            search_input,
            image_list,
            ft.Row([prev_button, next_button], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        ]),
        actions=[
            ft.TextButton("Back", on_click=lambda e: close_dialog(image_selection_dialog, page, previous_dialog))
        ]
    )

    page.overlay.append(image_selection_dialog)
    image_selection_dialog.open = True
    page.update()

def close_dialog(dialog, page, previous_dialog=None):
    dialog.open = False
    page.update()
    if previous_dialog:
        previous_dialog.open = True
        page.update()
