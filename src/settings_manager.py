from data_handler import set_create_setting, get_create_setting
import flet as ft


class Checkbox(ft.UserControl):
    def __init__(self, name, label):
        super().__init__()
        self.name = name
        self.label = label

    def get_value(self):
        return self.checkbox.value

    def build(self):
        self.checkbox = ft.Checkbox(
            label=self.label,
            on_change=lambda _:
            set_create_setting(self.name, self.get_value())
        )
        return self.checkbox


class SettingsPage(ft.UserControl):
    def __init__(self, app, page: ft.Page):
        super().__init__()
        self.app = app
        self.page = page
        self.file_picker = ft.FilePicker(on_result=self.on_dialog_result)
        self.path_text = ft.Text(get_create_setting('dir_path'))
        self.add_path_bttn = ft.ElevatedButton(
                    text='Выбрать директорию',
                    style=ft.ButtonStyle(shape=ft.StadiumBorder()),
                    on_click=lambda _: self.file_picker.get_directory_path(),
                )
        self.create_checkboxes = [
            ('pip_setting', 'Обновлять pip'),
            ('main_setting', 'Создавать main.py'),
            ('vs_code_setting', 'Открывать проекты в VS Code')
        ]

        self.page.overlay.append(self.file_picker)

    def set_create_checkboxes(self):
        checkboxes_list = []
        for name, label in self.create_checkboxes:
            checkbox_view = Checkbox(name, label).build()
            if value := get_create_setting(setting=name):
                checkbox_view.value = value
            checkboxes_list.append(checkbox_view)
        return checkboxes_list

    def on_dialog_result(self, e: ft.FilePickerResultEvent):
        if e.path:
            self.path_text.value = e.path
            self.add_path_bttn.text = 'Изменить'
            set_create_setting('dir_path', e.path)
            self.page.update()

    def build(self):
        path_setting = ft.Row(
            [
                ft.Text('Расположение проектов: '),
                self.path_text,
                self.add_path_bttn
            ],
        )
        view = ft.Column(
            [
                ft.Text('Создание проектов'),
                ft.Divider(height=2),
                path_setting,
            ],
            alignment=ft.MainAxisAlignment.START,
            expand=True
        )

        create_checkboxes = self.set_create_checkboxes()
        if create_checkboxes:
            for checkbox in create_checkboxes:
                view.controls.append(checkbox)

        return view
