from data_operations import load_data, update_create_settings
from typing import Union
import re
import os
import datetime
import shutil
import subprocess


def check_string(input_string: str) -> bool:
    """
    Проверяет, содержит ли строка только буквы (как строчные, так и заглавные),
    цифры или символ подчеркивания.

    Аргументы:
    input_string (str): Строка для проверки.

    Возвращает:
    bool: True, если строка удовлетворяет критериям (содержит только буквы,
    цифры или символ подчеркивания), иначе False.
    """
    pattern = r'^[a-zA-Z0-9_]+$'
    if re.match(pattern, input_string):
        return True
    else:
        return False


def set_create_setting(setting: str, value: str):
    """
    Устанавливает значение определенного параметра в файле настроек
    'settings.json'.

    Аргументы:
    setting (str): Наименование параметра, значение которого нужно установить.
    value (str): Значение, которое следует установить для данного параметра.

    Примечание:
    Функция использует вспомогательную функцию update_create_settings
    для обновления файла настроек.

    Возвращает:
    None
    """
    update_create_settings(setting, value, 'settings.json')


def get_project_path(dir_path: str, project_name: str) -> str:
    """
    Возвращает путь к проекту, составленный из указанного каталога и
    имени проекта.

    Аргументы:
    dir_path (str): Путь к каталогу, в котором расположен проект.
    project_name (str): Имя проекта.

    Возвращает:
    str: Полный путь к проекту, составленный из указанного каталога и
    имени проекта.
    """
    project_path = os.path.join(dir_path, project_name)
    return project_path


def get_create_setting(setting: str) -> any:
    """
    Получает значение определенного параметра из файла настроек
    'settings.json'.

    Аргументы:
    setting (str): Наименование параметра, значение которого нужно получить.

    Возвращает:
    any: Значение указанного параметра из файла настроек, если оно существует,
    иначе None.
    """
    data: dict = load_data('settings.json')
    if data:
        data = data.get('create_settings')
        value = data.get(setting)
        return value
    else:
        return None


def create_venv(project_path: str):
    """
    Создает виртуальное окружение для проекта.

    Аргументы:
    project_path (str): Путь к каталогу проекта, где будет создано
    виртуальное окружение.

    Примечание:
    Функция создает каталог проекта, если он не существует.
    Затем переходит в этот каталог
    и использует команду Python для создания виртуального окружения (venv).
    Затем активирует виртуальное окружение.

    Возвращает:
    None
    """
    if not os.path.exists(project_path):
        os.makedirs(project_path)
    os.chdir(project_path)
    os.system('python -m venv venv')
    os.system('venv\\Scripts\\activate')


def update_pip(project_path: str):
    """
    Обновляет установщик пакетов pip в виртуальном окружении проекта.

    Аргументы:
    project_path (str): Путь к каталогу проекта,
    содержащему виртуальное окружение.

    Примечание:
    Функция формирует команду для обновления установщика пакетов pip
    в виртуальном окружении и выполняет эту команду с помощью модуля os.

    Возвращает:
    None
    """
    command = f'{project_path}\\venv\\scripts\\'
    command += 'python.exe -m pip install --upgrade pip'
    os.system(command)


def install_libs(project_path: str, libs: list):
    """
    Устанавливает указанные библиотеки в виртуальном окружении проекта.

    Аргументы:
    project_path (str): Путь к каталогу проекта,
    содержащему виртуальное окружение.
    libs (list): Список названий библиотек для установки.

    Примечание:
    Функция формирует команду для установки библиотек с помощью pip
    в виртуальном окружении
    и выполняет эту команду с помощью модуля os.

    Возвращает:
    None
    """
    command = f'{project_path}\\venv\\scripts\\'
    command += 'python.exe -m pip install '
    command += ' '.join(libs)
    os.system(command)


def exit_cmd():
    """
    Выход из командной оболочки (cmd).

    Примечание:
    Функция использует системную команду 'exit' для выхода из
    командной оболочки (cmd).

    Возвращает:
    None
    """
    os.system('exit')


def create_main_py(project_path: str):
    """
    Создает файл main.py в указанном каталоге проекта.

    Аргументы:
    project_path (str): Путь к каталогу проекта, в котором
    нужно создать файл main.py.

    Примечание:
    Функция использует оператор with для открытия файла main.py
    в режиме записи ('w'), но не записывает в него данные.

    Возвращает:
    None
    """
    os.mkdir(f'{project_path}\\src')

    with open(f'{project_path}\\src\\main.py', 'w'):
        pass

    with open(f'{project_path}\\src\\autopep.py', 'w') as f:
        f.write('''
            import os
            import subprocess
            from pathlib import Path

            def format_with_autopep8(file_path):
                command = ['autopep8', '--in-place', '--aggressive', file_path]
                subprocess.run(command, check=True)

            def format_with_black(file_path):
                command = ['black', file_path]
                subprocess.run(command, check=True)

            def format_python_file(file_path):
                if not os.path.exists(file_path):
                    print(f'File not found: {file_path}')
                    return

                try:
                    print(f'File formatting: {file_path}')
                    format_with_autopep8(file_path)
                    # format_with_black(file_path)
                except subprocess.CalledProcessError as e:
                    print(f'Error while formatting file {file_path}: {e}')

            if __name__ == '__main__':
                # Determining the current directory
                current_directory = Path(__file__).resolve().parent

                # Current file name
                current_script = Path(__file__).name

                # Traversing all .py files in the current directory and its subdirectories
                for py_file in current_directory.rglob('*.py'):
                    # We skip the script itself
                    if py_file.name != current_script:
                        format_python_file(py_file)
            ''')


def save_checkbox_value(e, label: str, value: bool):
    """
    Сохраняет значение флажка (чекбокса) в файле настроек.

    Аргументы:
    e: Объект события, который инициировал вызов функции (не используется).
    label (str): Название параметра (настройки), который
    соответствует чекбоксу.
    value (bool): Значение чекбокса, которое нужно сохранить.

    Примечание:
    Функция вызывает другую функцию set_create_setting для сохранения
    значения чекбокса в файле настроек.

    Возвращает:
    None
    """
    set_create_setting(label, value)


def get_projects() -> list:
    """
    Возвращает список проектов, хранящихся в указанном каталоге.

    Возвращает:
    list: Список названий проектов, отсортированный
    по времени последнего изменения.
    """
    dir_path = get_create_setting(setting='dir_path')
    if dir_path:
        projects = []
        for project in os.listdir(dir_path):
            project_path = os.path.join(dir_path, project)
            if os.path.isdir(project_path):
                if 'venv' in os.listdir(project_path):
                    projects.append(project)
        if projects:
            sorted_projects: list = sorted(projects,
                                           key=lambda x: os.path.getmtime(
                                               os.path.join(dir_path,
                                                            x)))
            sorted_projects.reverse()
            return sorted_projects
    else:
        return []


def remove_project(project_name: str):
    """
    Удаляет проект с указанным именем из каталога проектов.

    Аргументы:
    project_name (str): Имя проекта, который нужно удалить.

    Примечание:
    Функция получает путь к каталогу проекта через get_create_setting,
    затем составляет путь к указанному проекту. После этого функция
    использует shutil.rmtree для рекурсивного удаления каталога проекта.

    Возвращает:
    None
    """
    dir_path = get_create_setting(setting='dir_path')
    if os.path.exists(dir_path):
        project_path = os.path.join(dir_path, project_name)
        shutil.rmtree(project_path)


def open_project(project_name: str):
    """
    Открывает проект с указанным именем в редакторе кода
    или файловом менеджере.

    Аргументы:
    project_name (str): Имя проекта, который нужно открыть.

    Примечание:
    Функция получает путь к каталогу проекта через get_create_setting и
    создает полный путь к указанному проекту.
    Затем она проверяет, установлены ли настройки для
    открытия проекта вVisual Studio Code.
    Если это так, она запускает Visual Studio Code с указанным проектом.
    В противном случае, она открывает каталог проекта в файловом менеджере.

    Возвращает:
    None
    """
    dir_path = get_create_setting(setting='dir_path')
    project_path = os.path.join(dir_path, project_name)
    if get_create_setting(setting='vs_code_setting'):
        local_appdata_path = os.environ['LOCALAPPDATA']
        vs_code_path = os.path.join(local_appdata_path, "Programs",
                                    "Microsoft VS Code", "Code.exe")
        subprocess.Popen([vs_code_path, project_path])
    else:
        os.system(f'explorer {project_path}')


def get_dir_creation_date(project_name: str) -> Union[str, None]:
    """
    Получает дату и время создания каталога проекта.

    Аргументы:
    project_name (str): Имя проекта, для которого нужно получить дату
    и время создания каталога.

    Возвращает:
    str or None: Строка с датой и временем создания каталога
    в формате "%d.%m.%Y %H:%M", если каталог существует,
    в противном случае возвращает None.
    """
    dir_path = get_create_setting(setting='dir_path')
    dir_path = os.path.join(dir_path, project_name)
    if os.path.exists(dir_path):
        timestamp = os.path.getctime(dir_path)
        date = datetime.datetime.fromtimestamp(timestamp)
        date = date.strftime("%d.%m.%Y %H:%M")
        return date
    else:
        return None


def get_dir_modified_date(project_name: str) -> Union[str, None]:
    """
    Получает дату и время последнего изменения каталога проекта.

    Аргументы:
    project_name (str): Имя проекта, для которого нужно получить дату
    и время последнего изменения каталога.

    Возвращает:
    str or None: Строка с датой и временем последнего изменения каталога
    в формате "%d.%m.%Y %H:%M", если каталог существует,
    в противном случае возвращает None.
    """
    dir_path = get_create_setting(setting='dir_path')
    dir_path = os.path.join(dir_path, project_name)
    if os.path.exists(dir_path):
        timestamp = os.path.getmtime(dir_path)
        date = datetime.datetime.fromtimestamp(timestamp)
        date = date.strftime("%d.%m.%Y %H:%M")
        return date
    else:
        return None
