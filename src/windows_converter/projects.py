"""Project classes for Windows converter."""

import contextlib
from tkinter import messagebox
import json
import os
import shutil
from pathlib import Path

from windows_converter.constants import PROJECT_FILE, USER_DATA_DIR
from windows_converter.config import TomlConfig
from windows_converter.build import build_project
from windows_converter import logger


class Project():
    def __init__(self, data: dict = None) -> None:
        if data is None:
            data = {}
        self.id: str = ''
        self.name = ''
        self.description = ''
        self.author = ''
        self.email = ''

        self.dev_base_dir = ''
        self.dev_source_dir = ''
        self.dev_image_dir = ''
        self.tests_directory = ''

        self.win_source_dir = ''

        self.win_install_path = ''
        self.start_menu_text = ''
        self.company_name = ''
        self.exe_name = ''
        self.version = '0.0.0'
        self.status_ok = 1

        if data and isinstance(data, dict):
            self._assign_attributes(data)

        if self.dev_base_dir:
            self._get_directories()

    def _assign_attributes(self, data: dict) -> None:
        for key, item in data.items():
            setattr(self, key, item)

    def _get_windows_dir(self) -> str:
        # pylint: disable=no-member)
        if self.company_name:
            return (
                f'{self.config.windows_project_directory}\\'
                f'{self.company_name.lower()}\\'
                f'{self.name}')

        return f'{self.config.windows_project_directory}\\{self.name}'

    def __repr__(self):
        return f'Project: {self.name}'

    def _get_directories(self) -> None:
        if not self.dev_source_dir:
            self._get_src_directory()
        if not self.dev_image_dir:
            self._get_image_directory()
        if not self.tests_directory:
            self._get_tests_directory()

    def _get_src_directory(self) -> None:
        names = ['src', 'source']
        self.dev_source_dir = self._get_dir(names)

    def _get_image_directory(self) -> None:
        names = ['images']
        self.dev_image_dir = self._get_dir(names)

    def _get_tests_directory(self) -> None:
        names = ['tests']
        self.tests_directory = self._get_dir(names)

    def _get_dir(self, names: list[str]) -> str:
        for directory_name, subdir_list, _ in os.walk(
                self.dev_base_dir):
            for subdir_name in subdir_list:
                if subdir_name in names:
                    return str(Path(directory_name, subdir_name))

    def _name_upper(self, delimiter: str = '') -> str:
        words = self.name.split('_')
        upper = [word.capitalize() for word in words]
        return delimiter.join(upper)

    def build(
            self,
            config: TomlConfig,
            update_requirements: bool = False,
            testing: bool = False,
            ) -> int:

        return build_project(
            self,
            config,
            update_requirements,
            testing,)

    def _validate_icons(self, src_dir: Path, testing: bool) -> None:
        dirs = [dir.name for dir in Path(self.dev_source_dir).iterdir()
                if dir.is_dir()]
        if 'images' in dirs and not testing:
            dlg = messagebox.askyesno(
                '',
                'images is a directory in src. Copy?'
            )
            if not dlg:
                shutil.rmtree(Path(src_dir, 'images'))
        if testing and Path(src_dir, 'images').is_dir():
            shutil.rmtree(Path(src_dir, 'images'))

        images_dir = Path(Path(self.dev_source_dir), 'images')
        if (not Path(images_dir, 'icon.ico').is_file()
                or not Path(images_dir, 'icon.png').is_file()):
            dlg = messagebox.showerror(
                '',
                'icon.ico or icon.png not in images directory'
            )


class ProjectServer():
    def __init__(self, path: str = '') -> None:
        self.projects = []
        if not path:
            path = PROJECT_FILE
        self.path = path
        if self.path:
            self.projects = self.read_projects()

    def read_projects(self) -> list[Project]:
        projects = {}
        try:
            with open(PROJECT_FILE, 'r', encoding='utf-8') as f_projects:
                raw_data = json.load(f_projects)
            for id, data in raw_data.items():
                project = Project(data)
                project.id = id
                projects[id] = project
        except FileNotFoundError:
            logger.error(f'{PROJECT_FILE} FileNotFoundError')
        except IsADirectoryError:
            logger.error(f'{PROJECT_FILE} IsADirectoryError')
        except json.decoder.JSONDecodeError:
            logger.error(f'{PROJECT_FILE} JSONDecodeError')
        return projects

    def save_projects(self, projects: list[Project] = None) -> None:
        with contextlib.suppress(FileExistsError):
            os.makedirs(USER_DATA_DIR)
        if not projects:
            projects = self.projects

        projects_dict = {project.id: vars(project)
                         for project in projects.values()}
        with open(PROJECT_FILE, 'w', encoding='utf-8') as f_projects:
            json.dump(projects_dict, f_projects)
