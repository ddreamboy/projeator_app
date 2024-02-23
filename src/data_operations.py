import json
import os


def make_dir(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


def get_appdata_path(app_name='MyApp') -> str:
    appdata_path = os.getenv('APPDATA')
    project_data_path = os.path.join(appdata_path, 'LocalLow', 'ddb_apps',
                                     app_name)
    make_dir(project_data_path)
    return project_data_path


def load_data(filename: str):
    '''
    Функция загрузки данных

    Args:
        filenam (str): Имя файла загрузки.
        var_name (str): Имя конкретной переменной для загрузки.

    '''
    project_data_path = get_appdata_path(app_name='ProjCreator')
    data_path = os.path.join(project_data_path, filename)
    if os.path.exists(data_path):
        with open(data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data


def save_data(data: dict, filename: str):
    '''
    Метод сохранения данных

    Args:
        data (dict): Данные для сохранения.
        filenam (str): Имя файла сохранения.

    '''
    project_data_path = get_appdata_path(app_name='ProjCreator')
    data_path = os.path.join(project_data_path, filename)
    with open(data_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def update_data(data_upd: dict, filename: str):
    '''
    Функция обновления данных

    Args:
        data_upd (dict): Данные для обновления.
        filenam (str): Имя файла обновления.
        specific_key (str): Ключ для доступа к конкретной группе настроек.

    '''
    data: dict = load_data(filename)
    data.update(data_upd)
    save_data(data, filename)


def update_create_settings(setting: str, value, filename: str):
    '''
    Функция обновления данных

    Args:
        data_upd (dict): Данные для обновления.
        filenam (str): Имя файла обновления.
        specific_key (str): Ключ для доступа к конкретной группе настроек.

    '''
    data: dict = load_data(filename)
    try:
        data['create_settings'][setting] = value
    except Exception:
        data = {
            'create_settings': {
                setting: value
            }
        }
    save_data(data, filename)
