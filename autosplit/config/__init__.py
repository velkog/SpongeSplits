from typing import Any, Dict, Optional
from yaml import safe_load, YAMLError

CONFIG: Optional[Dict[str, Any]] = None
CONFIG_PATH: str = "autosplit/config/config.yaml"
DEBUG: bool


def get_config() -> Optional[Dict[str, Any]]:
    global CONFIG

    if CONFIG:
        return CONFIG

    with open(CONFIG_PATH, 'r') as stream:
        try:
            CONFIG = safe_load(stream)
            return CONFIG
        except YAMLError as exec:
            # TODO: this will cause a thread/process to crash, do something smarter
            # or maybe just reraise?
            # TODO: yell at the user that they need a config file if it doesn't exist
            return None


def get_route():
    return get_config()["route"]


local_config = get_config()
assert local_config is not None
CONFIG = local_config
DEBUG = CONFIG["debug"]
assert type(DEBUG) is bool
