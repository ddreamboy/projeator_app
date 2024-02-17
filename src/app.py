import flet as ft
from build_elements import (file_picker, builder,
                            checkboxes, texts,
                            buttons, projects_table)


def main(page: ft.Page):
    page.window_always_on_top = True
    page.window_width = 816
    page.window_height = 540
    page.window_resizable = False
    page.overlay.append(file_picker)

    builder()

    def route_change(index):
        if index == 0:
            top_bar = ft.Row(
                [
                    texts['projects_MyProjects'],
                    ft.Row([buttons['add_project_bttn']],
                           alignment=ft.MainAxisAlignment.END,
                           expand=1)
                ],
            )

            body = ft.Column(
                [
                    top_bar,
                    ft.Divider(height=2),
                    ft.Column([projects_table],
                              scroll=ft.ScrollMode.AUTO,
                              expand=1,
                              ),
                ],
                spacing=10,
                expand=1,
            )

            if len(page_content.controls) > 2:
                page_content.controls.pop()
            page_content.controls.append(body)
            page.route = '/projects'
            page.update()

        if index == 1:
            path_setting = ft.Row(
                    [
                        texts['settings_ProjectLocation'],
                        texts['path_text'],
                        buttons['add_path_bttn']
                    ],
            )

            body = ft.Column(
                [
                    texts['settings_ProjectsCreating'],
                    ft.Divider(height=2),
                    path_setting,
                    checkboxes['pip_setting'],
                    checkboxes['main_setting'],
                    checkboxes['open_setting'],
                    checkboxes['open_vs_code_setting'],
                    ft.Text(),
                    texts['settings_Interface'],
                    ft.Divider(height=2)
                ], alignment=ft.MainAxisAlignment.START,
                expand=True
            )

            if len(page_content.controls) > 2:
                page_content.controls.pop()
            page_content.controls.append(body)
            page.route = '/settings'
            page.update()

    rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        min_extended_width=400,
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
