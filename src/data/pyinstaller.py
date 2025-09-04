import PyInstaller.__main__
from pathlib import Path

HERE = Path(__file__).parent.absolute()
path_to_main = str(Path(HERE, 'main.py'))


def install():
    PyInstaller.__main__.run([
        path_to_main,
        '--onefile',
        '--windowed',
        '--name=<exe_name>.exe',
        '--icon=src/<project>/images/icon.ico',
        '--add-data=src/<project>/images/icon.png:images',
    ])
