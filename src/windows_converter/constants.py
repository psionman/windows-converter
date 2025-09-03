"""Constants for Windows converter."""
from pathlib import Path
from appdirs import user_config_dir, user_data_dir

from psiutils.known_paths import resolve_path

# General
AUTHOR = 'Jeff Watkins'
APP_NAME = 'windows_converter'
APP_AUTHOR = 'psionman'
HTML_DIR = resolve_path('html', __file__)
HELP_URI = ''

# Paths
CONFIG_PATH = Path(user_config_dir(APP_NAME, APP_AUTHOR), 'config.toml')
USER_DATA_DIR = user_data_dir(APP_NAME, APP_AUTHOR)
PROJECT_FILE = Path(USER_DATA_DIR, 'projects.json')
HOME = str(Path.home())

# GUI
APP_TITLE = 'Windows converter'
ICON_FILE = resolve_path('images/icon.png', __file__)

GEOMETRY = {
    'frm_main': {
        'Linux': '500x600',
        'Windows': '500x600',
    },
    'frm_project': {
        'Linux': '900x650',
        'Windows': '700x600',
    },
    'frm_config': {
        'Linux': '700x300',
        'Windows': '700x300',
    },
}
