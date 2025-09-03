import PyInstaller.__main__
from pathlib import Path

HERE = Path(__file__).parent.absolute()
path_to_main = str(Path(HERE, 'src', 'main.py'))


def install():
    PyInstaller.__main__.run([
        path_to_main,
        '--onefile',
        '--windowed',
        '--name=MinimalApp.exe',
        '--icon=minimal_app/images/icon.ico',
        '--add-data=minimal_app/images/icon.png:images',
    ])
