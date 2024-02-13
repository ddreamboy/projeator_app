import flet as ft
from data_manager import (load_data, update_data, get_appdata_path)


def main(page: ft.Page):
    page.window_always_on_top = True
    page.window_width = 816
    page.window_height = 528
    page.window_resizable = False


    settings = load_data('settings.json', var_name='create_settings')

    checkboxes = {}

    def save_checkbox_value(e):
        for key, checkbox in checkboxes.items():
            data_value = settings.get(key)
            if checkbox.value != data_value:
                data_upd = dict(create_settings={key: checkbox.value})
            update_data(data_upd, 'settings.json')
    
    def add_checkbox(name: str, *, label: str=None):
        checkbox = ft.Checkbox(
            label=label,
            on_change=save_checkbox_value
        )
        checkboxes.update({name: checkbox})
        
    def create_project():
        pass

    def on_dialog_result(e: ft.FilePickerResultEvent):
        if e.path:
            path_text.value = e.path
            add_path_bttn.text = 'Изменить'
            page.update()
            data_upd = dict(create_settings={'directory_path': path_text.value})
            update_data(data_upd, 'settings.json')


    file_picker = ft.FilePicker(on_result=on_dialog_result)
    page.overlay.append(file_picker)
    add_path_bttn = ft.ElevatedButton(text="Выбрать директорию",
                                    style=ft.ButtonStyle(
                                        shape=ft.StadiumBorder()),
                                    on_click=lambda _:
                                    file_picker.get_directory_path())
    add_project_bttn = ft.FloatingActionButton(
                        text="Создать проект",
                        icon=ft.icons.ADD_ROUNDED,
                        height=30,
                        on_click=lambda e:create_project())
    path_text = ft.Text()
    path_setting = ft.Row(
        [
            ft.Text('Расположение проектов:'), path_text, add_path_bttn
        ],
    )

    add_checkbox('pip_setting', label='Обновлять pip')
    add_checkbox('main_setting', label='Создавать main.py')
    add_checkbox('open_setting', label='Открывать директорию проекта после создания')


    def route_change(index):
        if index == 0:
            projects_bar = ft.Row(
                [
                    ft.Text('Мои проекты'),
                    ft.Row([add_project_bttn],
                        alignment=ft.MainAxisAlignment.END,
                        expand=1)
                ],
            )
            projects_view = ft.DataTable(
                columns=[
                    ft.DataColumn(ft.TextButton(content=ft.Icon(
                        ft.icons.OPEN_IN_NEW_ROUNDED,
                        color=ft.colors.TRANSPARENT
                        ),
                        disabled=True)),
                    ft.DataColumn(ft.Text('Название проекта')),
                    ft.DataColumn(ft.Text('Изменен')),
                    ft.DataColumn(ft.Text('Создан'))
                ],
                expand=1
            )

            projects = {
                '1': {
                    'name': 'good_morning_app',
                    'changed': '11.07.2023 15:02',
                    'created': '11.07.2023 15:02'
                    },
            }

            for key in projects.keys():
                project = projects.get(key)
                name = project.get('name')
                changed = project.get('changed')
                created = project.get('created')
                project_info = ft.DataRow(
                            cells=[
                                ft.DataCell(ft.TextButton(
                                    content=ft.Icon(
                                        ft.icons.OPEN_IN_NEW_ROUNDED))),
                                ft.DataCell(ft.Text(name)),
                                ft.DataCell(ft.Text(changed)),
                                ft.DataCell(ft.Text(created)),
                            ]
                        )
                projects_view.rows.append(project_info)

            body = ft.Column(
                [
                    projects_bar,
                    ft.Divider(height=2),
                    projects_view,
                ],
                spacing=10,
                expand=True,
            )
            if len(page_content.controls) > 2:
                page_content.controls.pop()
            page_content.controls.append(body)
            page.route = '/projects'
            page.update()

        if index == 1:
            for key, checkbox in checkboxes.items():
                setting = settings.get(key)
                if setting:
                    checkbox.value = setting
                    page.update()

            body = ft.Column(
                [
                    ft.Text('Создание проектов'),
                    ft.Divider(height=2),
                    ft.Row([path_setting]),
                ], alignment=ft.MainAxisAlignment.START,
                expand=True
            )
            body.controls = body.controls + list(checkboxes.values()) + [ft.Text(), ft.Text('Интерфейс'), ft.Divider(height=2)]
            if len(page_content.controls) > 2:
                page_content.controls.pop()
            page_content.controls.append(body)
            page.route = '/settings'
            if settings:
                directory_path = settings.get('directory_path') 
                if directory_path:
                    path_text.value = directory_path
                    add_path_bttn.text = 'Изменить'
            page.update()

    
    rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        min_extended_width=400,
        # leading=ft.Row([
        #             ft.Image(
        #                 src="icons\\logo.png",
        #                 fit=ft.ImageFit.COVER,
        #                 repeat=ft.ImageRepeat.NO_REPEAT,
        #                 width=64,
        #                 height=64
        #                 )
        #         ]),
        group_alignment=-1,
        destinations=[
            ft.NavigationRailDestination(
                icon_content=ft.Icon(ft.icons.FOLDER_OUTLINED),
                selected_icon_content=ft.Icon(ft.icons.FOLDER),
                label="Проекты",
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.SETTINGS_OUTLINED,
                selected_icon_content=ft.Icon(ft.icons.SETTINGS),
                label_content=ft.Text("Настройки"),
            ),
        ],
        on_change=lambda e: route_change(e.control.selected_index),
    )
    page_content = ft.Row(
        controls=[rail, ft.VerticalDivider(width=1)],
        expand=True
    )
    route_change(0)
    page.add(page_content)


ft.app(target=main)
