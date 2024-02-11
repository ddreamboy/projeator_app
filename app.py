import flet as ft
import subprocess
import os

def main(page: ft.Page):
    page.title = "Projeator"
    page.window_always_on_top = True
    page.window_height = 512
    page.window_width = 384
    page.window_resizable = False
    page.theme = ft.Theme(color_scheme_seed='white')
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER
    
    
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
        path_text.value = pars_path(e.path)
        page.client_storage.set('path', e.path)
        page.update()
        
    def create_project():
        path_text.visible = False
        change_path_bttn.visible = False
        project_name.visible = False
        create_project_bttn.visible = False
        libs_text.visible = False
        for lib in libs:
            lib.visible = False
        process_text.value = 'Cоздаю директорию проекта...'
        page.update()
        directory = f'{path_text.value}\\{project_name.value}'
        os.mkdir(directory)
        process_text.value = 'Настраиваю виртуальное окружение...'
        page.update()
        command = ["python", "-m", "venv", "venv"]
        cwd = directory
        subprocess.run(command, cwd=cwd)
        command_activate = "venv\\Scripts\\activate" if os.name == 'nt' else "source venv/bin/activate"
        process_text.value = 'Обновляю pip...'
        page.update()
        command_upgrade_pip = ["python", "-m", "pip", "install", "--upgrade", "pip"]
        subprocess.run(command_activate, cwd=directory, shell=True)
        subprocess.run(command_upgrade_pip, cwd=directory)
        packages = [lib.label for lib in libs if lib.value == True]  # Список пакетов для установки
        
        if len(packages) > 1:
            process_text.value = 'Загружаю библиотеки...'
            page.update()
        elif len(packages) == 1:
            process_text.value = f'Загружаю {packages[0]}...'
            page.update()
        
        if len(packages) > 0:
            command_activate = "venv\\Scripts\\activate" if os.name == 'nt' else "source venv/bin/activate"
            command_install_packages = ["pip", "install"] + packages
            subprocess.run(command_activate, cwd=directory, shell=True)
            subprocess.run(command_install_packages, cwd=directory)

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
    
    if page.client_storage.get('path') != None:
        path_text.value = pars_path(page.client_storage.get('path'))
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



def pars_path(path):
    path_dirs = path.split('\\')
    if len(path) > 30:
        path = f'{path_dirs[0]}/.../{path_dirs[-1]}'
    return path

ft.app(target=main)