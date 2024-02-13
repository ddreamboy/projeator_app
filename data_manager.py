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


def load_data(filename: str, *, var_name=None):
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
            except json.JSONDecodeError as e:
                return None
    else:
        return None


def save_data(data: dict, filename: str):
    project_data_path = get_appdata_path()
    data_path = os.path.join(project_data_path, filename)
    with open(data_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def update_data(data_upd: dict, filename: str):
    '''
    Функция обновления данных

    Args:
        data_upd (dict): Данные для обновления.
        filenam (str): Имя файла обновления.

    '''
    data: dict = load_data(filename)
    if data:
        data.get(list(data_upd.keys())[0]).update(list(data_upd.values())[0])
    else:
        data = data_upd
    save_data(data, filename)
