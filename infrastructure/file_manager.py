import os
import sys


def create_app_base_directory(config):
    drive = config.get("app_drive")
    app_base_directory_name = config.get("app_base_directory_name")
    app_base_directory_path = f"{drive}/{app_base_directory_name}"
    if not os.path.exists(app_base_directory_path):
        try:
            os.makedirs(app_base_directory_path)
        except PermissionError:
            print(f"ERROR: Cannot create base directory at {app_base_directory_path}")


def get_file_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
