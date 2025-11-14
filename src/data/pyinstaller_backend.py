

from pathlib import Path
import PyInstaller.__main__


class _Backend:
    def build_wheel(
            self,
            wheel_directory,
            config_settings=None,
            metadata_directory=None):
        self._run_pyinstaller()
        import setuptools.build_meta
        return setuptools.build_meta.build_wheel(
            wheel_directory, config_settings, metadata_directory
        )

    def build_sdist(self, sdist_directory, config_settings=None):
        self._run_pyinstaller()
        import setuptools.build_meta
        return setuptools.build_meta.build_sdist(
            sdist_directory, config_settings)

    def prepare_metadata_for_build_wheel(
            self, metadata_directory, config_settings=None):
        import setuptools.build_meta
        return setuptools.build_meta.prepare_metadata_for_build_wheel(
            metadata_directory, config_settings
        )

    # ------------------------------------------------------------------
    def _run_pyinstaller(self):
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


# PEP-517 expects this object
backend = _Backend()
