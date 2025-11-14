import PyInstaller.__main__
from pathlib import Path

def main() -> None:
    HERE = Path(__file__).parent
    MAIN = HERE / "main.py"
    DIST = Path.cwd() / "dist"

    print("\nBuilding <exe_name>.exe with PyInstaller...")
    PyInstaller.__main__.run([
        str(MAIN),
        "--onefile",
        "--windowed",
        "--name=<exe_name>",
        "--icon=images/phoenix.ico",
        "--add-data=images/phoenix.png:images",
        f"--distpath={DIST}",
    ])
    print(f"Executable created: {DIST / '<exe_name>.exe'}\n")

if __name__ == "__main__":
    main()
