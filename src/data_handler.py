from data_operations import load_data, update_data
import os
import datetime


def get_create_settings(*, setting: str = None):
    data = load_data('settings.json', var_name='create_settings')
    if data:
        if setting:
            value = data.get(setting)
            return value
        else:
            return data


def set_create_settings(setting: str, value):
    data = {
        setting: value
    }
    update_data(data, 'settings.json', specific_key='create_settings')


def get_projects():
    try:
        directory_path = get_create_settings(setting='directory_path')
    except Exception:
        directory_path = None
    if directory_path:
        projects = {}
        for project in os.listdir(directory_path):
            project_path = os.path.join(directory_path, project)
            if os.path.isdir(project_path):
                if 'venv' in os.listdir(project_path):
                    name = project
                    created = get_directory_creation_date(project_path)
                    modified = get_directory_last_modified_date(project_path)
                    projects.update({
                        name: {
                            'modified': modified,
                            'created': created
                        }
                    })
        return projects
    return None


def get_directory_creation_date(path):
    if os.path.exists(path):
        timestamp = os.path.getctime(path)
        date = datetime.datetime.fromtimestamp(timestamp)
        date = date.strftime("%d.%m.%Y %H:%M")
        return date
    else:
        return None


def get_directory_last_modified_date(path):
    if os.path.exists(path):
        timestamp = os.path.getmtime(path)
        date = datetime.datetime.fromtimestamp(timestamp)
        date = date.strftime("%d.%m.%Y %H:%M")
        return date
    else:
        return None
