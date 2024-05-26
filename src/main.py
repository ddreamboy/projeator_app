from app_layout import AppLayout
import flet as ft
import pyautogui


class ProjCreatorApp(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.page.on_route_change = self.route_change

    def build(self):
        self.layout = AppLayout(self, self.page)
        return self.layout

    def refresh_projects(self):
        body = self.layout.set_projects_view()
        self.page_content.controls[-1] = body
        self.page.update()

    def route_change(self, e):
        troute = ft.TemplateRoute(self.page.route)
        if troute.match("/"):
            self.page.go("/projects")
        elif troute.match("/projects"):
            body = self.layout.set_projects_view()
            self.page_content.controls[-1] = body
        elif troute.match("/settings"):
            body = self.layout.set_settings_view()
            self.page_content.controls[-1] = body
        self.page.update()

    def initialize(self):
        body = self.layout.set_projects_view()
        self.page_content = ft.Row(
            controls=[
                self.layout.sidebar,
                ft.VerticalDivider(width=1),
                body
            ],
            expand=True
            )
        self.page.add(self.page_content)
        self.page.update()
        self.page.go("/")


def main(page: ft.Page):
    page.title = "ProjCreator"
    page.window_width = 816
    page.window_height = 540
    screen_width, screen_height = pyautogui.size()
    page.window_top = (screen_height / 2) - (page.window_height / 1.5)
    page.window_left = (screen_width / 2) - (page.window_width / 2)
    page.window_resizable = False
    app = ProjCreatorApp(page)
    page.add(app)
    page.update()
    app.initialize()


ft.app(target=main)
