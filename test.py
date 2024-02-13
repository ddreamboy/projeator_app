from data_manager import update_data


data = {
    'create_settings': {
        'directory_path': None,
        'pip_setting': False,
        'main_setting': False,
        'open_setting': False,
    }
}

update_data(data, 'settings.json')
