import json
import os


def get_appdata_path(*, appdata_path=None) -> str:
    app_name = 'Projeator'
    if not appdata_path:
        appdata_path = os.getenv('APPDATA')
    project_data_path = os.path.join(appdata_path, 'LocalLow', 'ddb_apps',
                                     app_name)
    if not os.path.exists(project_data_path):
        os.makedirs(project_data_path)
    return project_data_path


def load_data(filename: str, *, var_name: str = None):
    '''
    Функция загрузки данных

    Args:
        filenam (str): Имя файла загрузки.
        var_name (str): Имя конкретной переменной для загрузки.

    '''
    project_data_path = get_appdata_path()
    data_path = os.path.join(project_data_path, filename)
    if os.path.exists(data_path):
        if var_name:
            with open(data_path, 'r', encoding='utf-8') as f:
                data: dict = json.load(f)
            var = data.get(var_name)
            return var
        else:
            try:
                with open(data_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                return data
            except json.JSONDecodeError:
                return None
    else:
        return None


def save_data(data: dict, filename: str):
    '''
    Метод сохранения данных

    Args:
        data (dict): Данные для сохранения.
        filenam (str): Имя файла сохранения.

    '''
    project_data_path = get_appdata_path()
    data_path = os.path.join(project_data_path, filename)
    with open(data_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def update_data(data_upd: dict, filename: str, *, specific_key: str = None):
    '''
    Функция обновления данных

    Args:
        data_upd (dict): Данные для обновления.
        filenam (str): Имя файла обновления.
        specific_key (str): Ключ для доступа к конкретной группе настроек.

    '''
    data: dict = load_data(filename)
    if specific_key:
        specific_data: dict = data.get(specific_key)
        specific_data.update(data_upd)
        data.update({specific_key: specific_data})
    else:
        data = data_upd
    save_data(data, filename)
