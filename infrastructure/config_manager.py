import json
import os
import sys
from infrastructure.config_defaults import config_defaults

_config_cache = None


def _load_from_disk():
    app_dir = "";
    if getattr(sys, "frozen", False):
        app_dir = os.path.dirname(sys.executable)
    else:
        utils_dir = os.path.dirname(os.path.abspath(__file__))
        app_dir = os.path.dirname(utils_dir)

    config_path = os.path.join(app_dir, "config.json")

    print(f"DEBUG: Looking for config at: {config_path}")

    defaults = config_defaults

    if os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                defaults.update(data)
        except Exception as e:
            print(f"Error reading config JSON: {e}")
    else:
        print(f"ERROR: config.json not found at {config_path}, using config_defaults")

    return defaults


def get_app_configuration():
    global _config_cache
    if _config_cache is None:
        _config_cache = _load_from_disk()
    return _config_cache


def get_config_value(key, default_val=None):
    config = get_app_configuration()
    return config.get(key, default_val)


