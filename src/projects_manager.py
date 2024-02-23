from dialogs import AddProjectModal, DeleteProjectModal
from data_handler import (
    get_projects,
    get_dir_creation_date,
    get_dir_modified_date,
    open_project
)
import flet as ft


class Project(ft.UserControl):
    def __init__(self, name, app, page):
        super().__init__()
        self.name = name
        self.app = app
        self.page = page
        self.modified_date = get_dir_modified_date(name)
        self.created_date = get_dir_creation_date(name)
        self.open_bttn = ft.TextButton(
                content=ft.Icon(ft.icons.OPEN_IN_NEW_ROUNDED),
                on_click=lambda _: open_project(self.name)
            )
        self.delete_bttn = ft.FloatingActionButton(
                icon=ft.icons.DELETE,
                height=25,
                width=25,
                bgcolor=ft.colors.TRANSPARENT,
                on_click=DeleteProjectModal(
                    self.app, self.page, self.name).open_dlg_modal,
            )

    def build(self):
        view = ft.DataRow(
            [
                ft.DataCell(self.open_bttn),
                ft.DataCell(ft.Row(
                    [
                        self.delete_bttn,
                        ft.Text(self.name)
                    ]
                )
                    ),
                ft.DataCell(ft.Text(self.modified_date)),
                ft.DataCell(ft.Text(self.created_date)),
            ]
        )
        return view


class ProjectsPage(ft.UserControl):
    def __init__(self, app, page):
        super().__init__()
        self.app = app
        self.page = page
        self.top_bar = ft.Row(
            [
                ft.Text('Мои проекты'),
                ft.Row([
                    ft.FloatingActionButton(
                        text='Создать проект',
                        icon=ft.icons.ADD_ROUNDED,
                        height=30,
                        on_click=AddProjectModal(app, page).open_dlg_modal
                    ),
                ], alignment=ft.MainAxisAlignment.END, expand=1,
                )
            ]
        )
        self.projects_table = ft.DataTable(
            columns=[
                ft.DataColumn(
                    ft.TextButton(
                        content=ft.Icon(ft.icons.OPEN_IN_NEW_ROUNDED,
                                        color=ft.colors.TRANSPARENT),
                        disabled=True)
                    ),
                ft.DataColumn(ft.Text('Название проекта')),
                ft.DataColumn(ft.Text('Изменен')),
                ft.DataColumn(ft.Text('Создан')),
            ]
        )

    def set_projects(self, projects_list):
        self.projects_table.rows = []
        for project in projects_list:
            project_view = Project(project, self.app, self.page).build()
            self.projects_table.rows.append(project_view)

    def build(self):
        view = ft.Column(
                [
                    self.top_bar,
                    ft.Divider(height=2),
                ],
                spacing=10,
                expand=1,
            )
        projects_list = get_projects()
        if projects_list:
            self.set_projects(projects_list)
            projects_view = ft.Column([self.projects_table],
                                      scroll=ft.ScrollMode.AUTO,
                                      expand=1,
                                      )
            view.controls.append(projects_view)
        return view
