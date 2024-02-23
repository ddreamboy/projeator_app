import flet as ft


class Sidebar(ft.UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.nav_items = [
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
        ]
        self.nav_rail = ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=100,
            min_extended_width=400,
            group_alignment=-1,
            destinations=self.nav_items,
            on_change=self.nav_change,
        )

    def build(self):
        view = self.nav_rail
        return view

    def nav_change(self, e):
        index = e.control.selected_index
        self.nav_rail.selected_index = index
        if index == 0:
            self.page.route = '/projects'
        elif index == 1:
            self.page.route = '/settings'
        self.page.update()
