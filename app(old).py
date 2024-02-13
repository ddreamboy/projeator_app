import flet as ft
import os
import json


def main(page: ft.Page):
    page.title = "Projeator"
    page.window_always_on_top = True
    page.window_height = 512
    page.window_width = 384
    page.window_resizable = False
    page.theme = ft.Theme(color_scheme_seed='white')
    page.vertical_alignment = ft.MainAxisAlignment.CENTER


    def create_project():
        if project_name.value:
            path_text.visible = False
            change_path_bttn.visible = False
            project_name.visible = False
            create_project_bttn.visible = False
            libs_text.visible = False
            for lib in libs:
                lib.visible = False

            dir_path = load_data('data.json', var_name='directory_path')
            directory = f'{dir_path}\\{project_name.value}'
            packages = [lib.label for lib in libs if lib.value is True]
            packages = ', '.join(packages)

            print(os.getcwd())
            commands: list = load_data('data.json', var_name='commands')
            statuses = load_data('data.json', var_name='loading_statuses')
            update_status(statuses.get('creating'))
            os.mkdir(directory)
            os.chdir(directory)
            for command in commands:
                cmd: str = command.get('command')
                status: str = command.get('status')
                if '{directory}' in cmd:
                    cmd = cmd.replace('{directory}', directory)
                    if status == 'upd_pip':
                        update_status(statuses.get(status))
                        os.system(cmd)
                if '{packages}' in cmd and packages != '':
                    cmd = cmd.replace('{packages}', packages)
                    if status == 'load_libs':
                        update_status(statuses.get(status))
                        os.system(cmd)
                else:
                    if status:
                        update_status(statuses.get(status))
                    os.system(cmd)

            with open(os.path.join(directory, 'main.py'), 'w'):
                pass

            complete_bttn.visible = True
            process_text.value = ''
            page.update()

    def completed():
        path_text.visible = True
        change_path_bttn.visible = True
        project_name.visible = True
        create_project_bttn.visible = True
        libs_text.visible = True
        for lib in libs:
            lib.visible = True
            lib.value = False
        complete_bttn.visible = False

        project_name.value = ''
        project_name.focus()
        page.update()

    def update_status(state: str):
        process_text.value = state
        page.update()

    def on_dialog_result(e: ft.FilePickerResultEvent):
        if add_path_bttn.visible:
            add_path_bttn.visible = False
        if not path_text.visible:
            path_text.visible = True
            change_path_bttn.visible = True
            project_name.visible = True
            create_project_bttn.visible = True
            libs_text.visible = True
            for lib in libs:
                lib.visible = True

        dir_path = e.path
        path_text.value = pars_path(dir_path)
        data = dict(directory_path=dir_path)
        update_data(data, 'data.json')
        page.update()
    file_picker = ft.FilePicker(on_result=on_dialog_result) 
    add_path_bttn = ft.ElevatedButton("Выбрать директорию",
                                      style=ft.ButtonStyle(
                                         shape=ft.StadiumBorder()),
                                      on_click=lambda _: file_picker.get_directory_path(),
                                      )
    change_path_bttn = ft.ElevatedButton("Изменить",
                                         style=ft.ButtonStyle(
                                             shape=ft.StadiumBorder()),
                                         on_click=lambda _: file_picker.get_directory_path(),
                                         visible=False
                                         )
    create_project_bttn = ft.ElevatedButton("Создать",
                                            style=ft.ButtonStyle(
                                                shape=ft.StadiumBorder()),
                                            on_click=lambda _: create_project(),
                                            visible=False
                                            )
    path_text = ft.Text(value='', visible=False)
    project_name = ft.TextField(hint_text='Название проекта',
                                border=ft.InputBorder.UNDERLINE,
                                visible=False,
                                width=200)
    libs_text = ft.Text('Выбери библиотеки (опционально)', visible=False)
    lib_0 = ft.Checkbox(label="numpy", value=False)
    lib_1 = ft.Checkbox(label="pandas", value=False)
    lib_2 = ft.Checkbox(label="matplotlib", value=False)
    lib_3 = ft.Checkbox(label="tensorflow", value=False)
    lib_4 = ft.Checkbox(label="scikit-learn", value=False)
    lib_5 = ft.Checkbox(label="requests", value=False)
    lib_6 = ft.Checkbox(label="seaborn", value=False)
    lib_7 = ft.Checkbox(label="flask", value=False)
    lib_8 = ft.Checkbox(label="pytest", value=False)
    libs = [lib_0, lib_1, lib_2, lib_3, lib_4, lib_5, lib_6, lib_7, lib_8]
    sub_libs = [ft.Column(libs[i:i+3]) for i in range(0, len(libs), 3)]

    process_text = ft.Text(value='')

    complete_bttn = ft.ElevatedButton("Готово",
                                      style=ft.ButtonStyle(
                                          shape=ft.StadiumBorder()),
                                      on_click=lambda _: completed(),
                                      visible=False
                                      )

    if load_data('data.json', var_name='directory_path'):
        dir_path = load_data('data.json', var_name='directory_path')
        path_text.value = pars_path(dir_path)
        add_path_bttn.visible = False
        path_text.visible = True
        change_path_bttn.visible = True
        project_name.visible = True
        create_project_bttn.visible = True
        libs_text.visible = True
    else:
        for lib in libs:
            lib.visible = False

    def row_with_alignment(align: ft.MainAxisAlignment, elements):
        return ft.Row(elements, alignment=align, spacing=10)

    page.add(row_with_alignment(ft.MainAxisAlignment.CENTER, [add_path_bttn]),
             row_with_alignment(ft.MainAxisAlignment.CENTER, [path_text]),
             row_with_alignment(ft.MainAxisAlignment.CENTER, [change_path_bttn]),
             row_with_alignment(ft.MainAxisAlignment.CENTER, [project_name, create_project_bttn]),
             row_with_alignment(ft.MainAxisAlignment.START, [libs_text]),
             ft.Row(sub_libs),
             row_with_alignment(ft.MainAxisAlignment.CENTER, [process_text]),
             row_with_alignment(ft.MainAxisAlignment.CENTER, [complete_bttn]),
             )
    page.overlay.append(file_picker)
    page.update()


def pars_path(path: str) -> str:
    if path:
        path_dirs = path.split('\\')
        if len(path) > 30:
            path = f'{path_dirs[0]}/.../{path_dirs[-1]}'
        return path


def load_data(filename: str, *, var_name=None):
    if var_name:
        with open(f'{filename}', 'r', encoding='utf-8') as f:
            data = json.load(f)
        var = data.get(var_name)
        return var
    else:
        with open(f'{filename}', 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data


def save_data(data: dict, filename: str):
    with open(f'{filename}', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def update_data(data_upd: dict, filename: str):
    data = load_data(filename)
    data.update(data_upd)
    save_data(data, filename)


ft.app(target=main)
