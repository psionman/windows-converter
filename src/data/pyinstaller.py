import PyInstaller.__main__
from pathlib import Path

HERE = Path(__file__).parent.absolute()
path_to_main = str(Path(HERE, '<project_dir>', 'main.py'))


def install():
    PyInstaller.__main__.run([
        path_to_main,
        '--onefile',
        '--windowed',
        '--name=<exe_name>.exe',
        '--icon=src/images/icon.ico',
        '--add-data=src/images/icon.png:images',
    ])
