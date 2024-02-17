from data_handler import (get_projects,
                          get_create_settings,
                          set_create_settings)
from data_operations import save_data, load_data
import os
import subprocess
import flet as ft

checkboxes = {}
texts = {}
buttons = {}
projects_table = ft.DataTable()
open_project_bttns_id = {}


def on_dialog_result(e: ft.FilePickerResultEvent):
    if e.path:
        texts['path_text'].value = e.path
        buttons['add_path_bttn'].text = 'Изменить'
        set_create_settings('directory_path', e.path)
        build_projects()


file_picker = ft.FilePicker(on_result=on_dialog_result)


def save_checkbox_value(e):
    for key, checkbox in checkboxes.items():
        data_value = get_create_settings(setting=key)
        if checkbox.value != data_value:
            set_create_settings(key, checkbox.value)


# TODO: реализовать удаление/переименование проектов
# + фильтрация по дате изменения
def create_project():
    pass


def open_project(id):
    project_name = open_project_bttns_id.get(id)
    directory_path = get_create_settings(setting='directory_path')
    project_path = os.path.join(directory_path, project_name)
    if get_create_settings(setting='open_vs_code_setting'):
        local_appdata_path = os.environ['LOCALAPPDATA']
        vs_code_path = os.path.join(local_appdata_path, "Programs",
                                    "Microsoft VS Code", "Code.exe")
        subprocess.Popen([vs_code_path, project_path])
    else:
        os.system(f'explorer {project_path}')


def load_values():
    for key, checkbox in checkboxes.items():
        data_value = get_create_settings(setting=key)
        checkbox.value = data_value
        checkboxes[key] = checkbox

    path_text: ft.Text = texts['path_text']
    path_text.value = get_create_settings(setting='directory_path')
    texts['path_text'] = path_text


checkbox_templates = {
    'pip_setting': {
        'label': 'Обновлять pip',
        },
    'main_setting': {
        'label': 'Создавать main.py',
        },
    'open_setting': {
        'label': 'Открывать директорию проекта после создания',
        },
    'open_vs_code_setting': {
        'label': 'Открывать проекты в VS Code',
        },
}

text_templates = {
    'path_text': {
        'value': ''
    },
    'settings_ProjectLocation': {
        'value': 'Расположение проектов:'
    },
    'settings_ProjectsCreating': {
        'value': 'Создание проектов'
    },
    'settings_Interface': {
        'value': 'Интерфейс'
    },
    'projects_MyProjects': {
        'value': 'Мои проекты'
    },
    'column_ProjectName': {
        'value': 'Название проекта'
    },
    'column_ProjectChanged': {
        'value': 'Изменен'
    },
    'column_ProjectCreated': {
        'value': 'Создан'
    },
}

button_templates = {
    'add_path_bttn': {
        'bttn_type': ft.ElevatedButton,
        'text': 'Выбрать директорию',
        'style': ft.ButtonStyle(shape=ft.StadiumBorder()),
        'on_click': lambda _: file_picker.get_directory_path(),
    },
    'add_project_bttn': {
        'bttn_type': ft.FloatingActionButton,
        'text': 'Создать проект',
        'icon': ft.icons.ADD_ROUNDED,
        'height': 30,
        'on_click': lambda _: create_project(),
    },
    'open_project_transp_bttn': {
        'bttn_type': ft.TextButton,
        'content': ft.Icon(ft.icons.OPEN_IN_NEW_ROUNDED,
                           color=ft.colors.TRANSPARENT),
        'disabled': True,
    },
    'open_project_bttn': {
        'bttn_type': ft.TextButton,
        'content': ft.Icon(ft.icons.OPEN_IN_NEW_ROUNDED),
        'disabled': False,
    }
}


def build_checkbox():
    for name, params in checkbox_templates.items():
        checkbox = ft.Checkbox(
            label=params.get('label'),
            on_change=save_checkbox_value
        )
        checkboxes.update({name: checkbox})


def build_texts():
    for name, params in text_templates.items():
        text = ft.Text(
            value=params.get('value'),
        )
        texts.update({name: text})


def build_buttons():
    for name, params in button_templates.items():
        bttn_type = params.get('bttn_type')
        if bttn_type == ft.ElevatedButton:
            button = ft.ElevatedButton(
                text=params.get('text'),
                style=params.get('style'),
                on_click=params.get('on_click')
            )
            buttons.update({name: button})
        if bttn_type == ft.FloatingActionButton:
            button = ft.FloatingActionButton(
                text=params.get('text'),
                icon=params.get('icon'),
                height=params.get('height'),
                on_click=params.get('on_click')
            )
            buttons.update({name: button})
        if bttn_type == ft.TextButton:
            button = ft.TextButton(
                content=params.get('content'),
                disabled=params.get('disabled')
            )
            buttons.update({name: button})


def build_projects():
    projects = get_projects()
    if projects:
        if buttons == {}:
            build_buttons()
        if texts == {}:
            build_texts

        element = ft.DataColumn(buttons.get('open_project_transp_bttn'))
        projects_table.columns.append(element)
        element = ft.DataColumn(texts.get('column_ProjectName'))
        projects_table.columns.append(element)
        element = ft.DataColumn(texts.get('column_ProjectChanged'))
        projects_table.columns.append(element)
        element = ft.DataColumn(texts.get('column_ProjectCreated'))
        projects_table.columns.append(element)

        ids_counter = 33
        for name, date in projects.items():
            project_open_bttn = ft.TextButton(
                content=ft.Icon(ft.icons.OPEN_IN_NEW_ROUNDED),
                on_click=lambda e: open_project(e.target)
            )
            project_name_cell = ft.DataCell(ft.Text(name))
            project_info = ft.DataRow(
                cells=[
                    ft.DataCell(project_open_bttn),
                    project_name_cell,
                    ft.DataCell(ft.Text(date.get('modified'))),
                    ft.DataCell(ft.Text(date.get('created'))),
                ]
            )
            projects_table.rows.append(project_info)
            id = f'_{ids_counter}'
            open_project_bttns_id.update({id: name})
            ids_counter += 10


def builder():
    data = {
        "create_settings": {
            "directory_path": None,
        }
    }

    if not load_data('settings.json'):
        save_data(data, 'settings.json')

    build_checkbox()
    build_buttons()
    build_texts()
    build_projects()

    load_values()
