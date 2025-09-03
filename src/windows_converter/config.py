"""Config for Windows converter."""
from pathlib import Path
from psiconfig import TomlConfig


from windows_converter.constants import CONFIG_PATH, USER_DATA_DIR, HOME

DEFAULT_CONFIG = {
    'data_directory': USER_DATA_DIR,
    'projects_directory': Path(HOME, 'projects'),
    'windows_base_directory': Path(HOME, 'projects', 'windows-projects'),
    'last_project': '',
    'author': '',
    'email': '',
    'windows_project_directory': '',
    'windows_installation': '',
    'geometry': {
        'frm_main': '500x600',
        'frm_project': '900x650',
        'frm_config': '700x300',
    },
}


def read_config(path: str = '') -> TomlConfig:
    """Return the config file."""
    if not path:
        path = CONFIG_PATH
    return TomlConfig(path=path, defaults=DEFAULT_CONFIG)

def save_config(toml_config: TomlConfig) -> TomlConfig | None:
    # NB new attributes need to be updated in gui.write_config
    result = toml_config.save()
    if result != toml_config.STATUS_OK:
        return None
    return TomlConfig(CONFIG_PATH)


config = read_config()
