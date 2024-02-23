from sidebar import Sidebar
from projects_manager import ProjectsPage
from settings_manager import SettingsPage
import flet as ft


class AppLayout(ft.Row):
    def __init__(self, app, page: ft.Page, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = app
        self.page = page
        self.sidebar = Sidebar(page)
        self.projects = ProjectsPage(app, page)
        self.settings = SettingsPage(app, page)

    def set_projects_view(self):
        body = self.projects.build()
        return body

    def set_settings_view(self):
        body = self.settings.build()
        return body
