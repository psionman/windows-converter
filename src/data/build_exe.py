import sys
import PyInstaller.__main__
from pathlib import Path
from PyInstaller.utils.hooks import collect_data_files
import time

SEP = '-'*100


def build() -> None:
    start_time = time.time()
    DIST = Path(Path.cwd(), 'dist')
    HERE = Path(__file__).parent
    MAIN = Path(HERE, 'main.py')
    ICON_ICO = Path(HERE, 'images', 'icon.png')

    sep = ';' if sys.platform == 'win32' else ':'

    psiutils_datas = collect_data_files('psiutils')

    print('\nBuilding <exe_name>.exe with PyInstaller...')

    # Start with base args
    args = [
        str(MAIN),
        '--onefile',
        '--windowed',
        '--name=<exe_name>',
        f'--icon={ICON_ICO}',
        f'--add-data={ICON_ICO}{sep}images',
        # f"--add-data={HERE / 'templates'}{sep}templates",
        f"--add-data={HERE / 'forms'}{sep}forms",
        f'--distpath={DIST}',
        '--clean',
        '--noconfirm',
        '--hidden-import=tkinter',
        '--hidden-import=tkinterweb',
        '--hidden-import=PIL._tkinter_finder',
    ]

    args.extend(f'--add-data={src}{sep}{dest}' for src, dest in psiutils_datas)
    PyInstaller.__main__.run(args)

    exe_path = DIST / '<exe_name>.exe'
    print(f'SUCCESS: {exe_path}')
    print(SEP)
    print(f'Time taken: {int(time.time() - start_time)} secs')
    print(SEP)


if __name__ == '__main__':
    build()
