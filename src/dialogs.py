from data_handler import (
    check_string,
    get_create_setting,
    get_project_path,
    create_venv,
    update_pip,
    install_libs,
    create_main_py,
    exit_cmd,
    remove_project
    )
import flet as ft


class AddProjectModal(ft.UserControl):
    def __init__(self, app, page: ft.Page):
        super().__init__()
        self.app = app
        self.page = page
        self.project_name = ft.TextField(
            label='Название проекта',
            height=40
        )
        self.lib_name = ft.TextField(
            label='Библиотека',
            height=40,
            width=170
        )

        self.libs = []
        self.libs_view = ft.ListView(spacing=10, auto_scroll=True)
        self.delete_lib_bttn = ft.FloatingActionButton(
            icon=ft.icons.DELETE,
            height=30,
            bgcolor=ft.colors.RED,
            on_click=lambda _: self.delete_lib(),
            visible=False,
            disabled=True
        )

        self.dlg_modal = ft.AlertDialog(
            title=ft.Text('Создание проекта'),
            content=ft.Column(
                [
                    self.project_name,
                    ft.Row([
                        self.lib_name,
                        ft.FloatingActionButton(
                            icon=ft.icons.ADD_ROUNDED,
                            height=30,
                            on_click=self.add_lib
                        )
                    ]),
                    self.libs_view,
                    self.delete_lib_bttn,
                    ft.Row(
                        [
                            ft.TextButton('Создать', on_click=self.close_dlg)
                        ],
                        alignment=ft.MainAxisAlignment.END,
                        ),
                ], tight=True, alignment="center"
            ),
        )

    def delete_lib(self):
        if self.libs:
            self.libs.pop()
            self.libs_view.controls.pop()
            if len(self.libs_view.controls) < 5:
                self.libs_view.expand = 0
            if len(self.libs) == 0:
                self.delete_lib_bttn.disabled = True
                self.delete_lib_bttn.visible = False
            self.page.update()

    def open_dlg_modal(self, e):
        self.page.dialog = self.dlg_modal
        self.dlg_modal.open = True
        self.page.update()

    def add_project(self, project_name: str, libs=[]):
        if check_string(project_name):
            status_text = ft.Text('Настраиваю виртуальное окружение',
                                  color=ft.colors.WHITE)
            dir_path = get_create_setting(setting='dir_path')
            project_path = get_project_path(dir_path, project_name)
            self.page.snack_bar = ft.SnackBar(ft.Row(
                [status_text],
                alignment=ft.MainAxisAlignment.CENTER
                ),
                bgcolor=ft.colors.BLACK87,
                duration=60_000
            )
            self.page.snack_bar.open = True
            self.page.update()

            create_venv(project_path)
            if get_create_setting(setting='pip_setting'):
                status_text.value = 'Обновляю pip...'
                self.page.update()
                update_pip(project_path)
            if libs:
                status_text.value = 'Устанавливаю библиотеки...'
                self.page.update()
                install_libs(project_path, libs)
            if get_create_setting(setting='main_setting'):
                create_main_py(project_path)

            exit_cmd()

            self.app.refresh_projects()

            status_text.value = 'Готово!'
            self.page.snack_bar = ft.SnackBar(ft.Row(
                [status_text],
                alignment=ft.MainAxisAlignment.CENTER
                ),
                bgcolor=ft.colors.BLACK87,
                duration=1000
                )
            self.page.snack_bar.open = True
            self.page.update()

    def close_dlg(self, e):
        self.dlg_modal.open = False
        self.page.update()
        if self.project_name.value:
            if self.libs:
                self.add_project(self.project_name.value, self.libs)
            else:
                self.add_project(self.project_name.value)
            self.project_name.value = ''

    def add_lib(self, e):
        lib = self.lib_name.value
        lib = lib.strip()
        if lib and lib not in self.libs:
            self.libs.append(lib)
            lib_view = ft.Row([
                ft.Icon(ft.icons.CHECK),
                ft.Text(lib, size=18),
            ])
            self.libs_view.controls.append(lib_view)
            if self.delete_lib_bttn.disabled:
                self.delete_lib_bttn.disabled = False
                self.delete_lib_bttn.visible = True
            if len(self.libs) > 5:
                self.libs_view.expand = 1
            else:
                self.libs_view.expand = 0
            self.lib_name.value = ''
        self.page.update()


class DeleteProjectModal(ft.UserControl):
    def __init__(self, app, page: ft.Page, project_name: str):
        super().__init__()
        self.app = app
        self.page = page
        self.project_name = project_name
        self.dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text('Требуется подтверждение'),
            content=ft.Text(f'Вы хотите удалить проект {project_name}?'),
            actions=[
                ft.TextButton('Да', on_click=self.remove),
                ft.TextButton('Нет', on_click=self.close_dlg),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

    def open_dlg_modal(self, e):
        self.page.dialog = self.dlg_modal
        self.dlg_modal.open = True
        self.page.update()

    def remove(self, e):
        remove_project(self.project_name)
        self.app.refresh_projects()
        self.close_dlg(e)

    def close_dlg(self, e):
        self.dlg_modal.open = False
        self.page.update()
