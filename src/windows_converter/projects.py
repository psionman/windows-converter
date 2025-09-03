"""Project classes for Windows converter."""
from tkinter import messagebox
from typing import NamedTuple
import json
import os
import shutil
from pathlib import Path

from psiutils.utilities import logger

from windows_converter.constants import PROJECT_FILE, USER_DATA_DIR
from windows_converter.config import TomlConfig, read_config


class ProjectData(NamedTuple):
    name: str
    description: str
    author: str
    exe_name: str
    windows_projects_directory: str
    project_development_directory: str
    src_directory: str
    image_directory: str
    windows_directory: str
    company_name: str
    installation_path: str
    start_menu_text: str


class Project():
    def __init__(self, data: ProjectData = None) -> None:
        if data is None:
            data = {}
        self.name = ''
        self.description = ''
        self.author = ''
        self.exe_name = ''
        self.windows_projects_directory = ''
        self.project_development_directory = ''
        self.src_directory = ''
        self.image_directory = ''
        self.tests_directory = ''
        self.windows_directory = ''
        self.company_name = ''
        self.installation_path = ''
        self.start_menu_text = ''
        self.version = '0.0.0'
        self.status_ok = 1

        if data:
            self._assign_attributes(data)

        if not self.windows_projects_directory:
            self.windows_projects_directory = self.name

        if self.project_development_directory:
            self.get_directories()

    def _assign_attributes(self, data: ProjectData) -> None:
        config = read_config()
        self.name = data.name
        self.windows_projects_directory = data.windows_projects_directory
        self.project_development_directory = data.project_development_directory
        self.src_directory = data.src_directory
        self.image_directory = data.image_directory
        self.windows_directory = data.windows_directory
        self.company_name = data.company_name
        self.start_menu_text = data.start_menu_text
        self.installation_path = data.installation_path
        self.exe_name = data.exe_name

        # Exe name
        if not self.exe_name:
            self.exe_name = self._name_upper('')

        # Author
        if not self.author:
            self.author = config.author

        # Description
        if not self.description:
            self.description = self._name_upper(' ')

        # Company name
        if not self.windows_directory:
            if self.company_name:
                self.windows_directory = (
                    f'{config.windows_project_directory}\\'
                    f'{self.company_name.lower()}\\'
                    f'{self.name}')
            else:
                self.windows_directory = (
                    f'{config.windows_project_directory}\\'
                    f'{self.name}')

        # Installation path
        if not self.installation_path:
            # if self.company_name:
            #     self.installation_path = (f'{self.company_name}\\'
            #                               f'{data.installation_path}')
            # else:
            self.installation_path = data.installation_path

    def __repr__(self):
        return f'Project: {self.name}'

    def serialize(self) -> tuple:
        return (
            self.name,
            self.description,
            self.author,
            self.exe_name,
            self.windows_projects_directory,
            self.project_development_directory,
            self.src_directory,
            self.image_directory,
            self.windows_directory,
            self.company_name,
            self.installation_path,
            self.start_menu_text,
        )

    def get_directories(self) -> None:
        if not self.src_directory:
            self._get_src_directory()
        if not self.image_directory:
            self._get_image_directory()
        if not self.tests_directory:
            self._get_tests_directory()

    def _get_src_directory(self) -> None:
        names = ['src', 'source']
        self.src_directory = self._get_dir(names)

    def _get_image_directory(self) -> None:
        names = ['images']
        self.image_directory = self._get_dir(names)

    def _get_tests_directory(self) -> None:
        names = ['tests']
        self.tests_directory = self._get_dir(names)

    def _get_dir(self, names: list[str]) -> str:
        for directory_name, subdir_list, _ in os.walk(
                self.project_development_directory):
            for subdir_name in subdir_list:
                if subdir_name in names:
                    return Path(directory_name, subdir_name)

    def _name_upper(self, delimiter: str = '') -> str:
        words = self.name.split('_')
        upper = [word.capitalize() for word in words]
        return delimiter.join(upper)

    def build(self, config: TomlConfig, testing: bool = False) -> None:
        windows_project_dir = Path(
            config.windows_base_directory, self.windows_projects_directory)
        target = Path(windows_project_dir).parts[-1]
        logger.debug((f'Building {self.project_development_directory} '
                     f'to {target}'))
        # print(f'Building {Path(windows_project_dir)}')

        # Remove old project
        if windows_project_dir.is_dir():
            shutil.rmtree(windows_project_dir)
        logger.debug('Removed old project')

        # Create project directory
        windows_project_dir.mkdir(parents=True, exist_ok=True)
        logger.debug('Created project')

        # Create the code directory
        # code_dir = Path(windows_project_dir, self.windows_projects_directory)
        code_dir = Path(windows_project_dir, 'src')
        code_dir.mkdir(parents=True, exist_ok=True)

        # Create the setup directory
        setup_dir = Path(windows_project_dir, 'setup')
        setup_dir.mkdir(parents=True, exist_ok=True)

        # Build src directory
        src_dir = Path(code_dir, self.windows_projects_directory)
        shutil.copytree(self.src_directory, src_dir, dirs_exist_ok=True)

        self._validate_icons(src_dir, testing)

        # Build images directory
        img_dir = Path(code_dir, 'images')
        shutil.copytree(self.image_directory, img_dir, dirs_exist_ok=True)

        # Build tests directory
        tests_dir = Path(windows_project_dir, 'tests')
        tests_dir.mkdir(parents=True, exist_ok=True)
        if self.tests_directory:
            shutil.copytree(
                self.tests_directory, tests_dir, dirs_exist_ok=True)
        logger.debug('Created project')

        # pyinstaller
        file_name = 'pyinstaller.py'
        code = self._get_text_file(file_name)
        code = code.replace('<exe_name>', self.exe_name)
        code = code.replace('<project_dir>', self.windows_projects_directory)
        target_file = Path(code_dir, file_name)
        self._save_text_file(target_file, code)

        # pyproject.toml
        file_name = 'pyproject.toml'
        code = self._get_text_file(file_name)
        code = code.replace('<description>', self.description)
        code = code.replace('<author>', self.author)
        code = code.replace('<project>', self.name)
        code = code.replace('<project_dir>', self.windows_projects_directory)
        code = code.replace('<version>', self.version)
        target_file = Path(windows_project_dir, file_name)
        self._save_text_file(target_file, code)

        # README
        file_name = 'README.md'
        code = ''
        target_file = Path(windows_project_dir, file_name)
        self._save_text_file(target_file, code)

        # InstallForge spec
        file_name = 'installforge.ifp'
        code = self._get_text_file(file_name)
        code = code.replace('<<name>>', self.description)
        code = code.replace('<<company name>>', self.company_name)
        code = code.replace(
            '<<windows directory>>', self.windows_directory)
        code = code.replace('<<exe name>>', self.exe_name)
        code = code.replace('<<installation path>>', self.installation_path)
        code = code.replace('<<version>>', self.version)
        code = code.replace('<<start menu text>>', self.start_menu_text)
        target_file = Path(windows_project_dir, f'{self.name}.ifp')
        self._save_text_file(target_file, code)

        # # requirements.txt
        requirements_source = Path(
            Path(self.project_development_directory).parent,
            'requirements.txt')
        if requirements_source.is_file():
            requirements_target = Path(
                Path(code_dir).parent, 'requirements.txt')
            shutil.copyfile(requirements_source, requirements_target)
        else:
            messagebox.showwarning(
                '',
                'No requirements file in project source directory'
            )

        logger.debug('Created text files')

        logger.debug('*** Build complete ***')

        return self.status_ok

    def _validate_icons(self, src_dir: Path, testing: bool) -> None:
        dirs = [dir.name for dir in Path(self.src_directory).iterdir()
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

        images_dir = Path(Path(self.src_directory), 'images')
        ic(images_dir)
        if (not Path(images_dir, 'icon.ico').is_file()
                or not Path(images_dir, 'icon.png').is_file()):
            dlg = messagebox.showerror(
                '',
                'icon.ico or icon.png not in images directory'
            )

    def _get_text_file(self, file_name: str) -> str:
        src_file = Path(Path(__file__).parent.parent, 'data', file_name)
        try:
            with open(src_file, 'r', encoding='utf-8') as f_source:
                return f_source.read()
        except FileNotFoundError:
            print(f'{src_file} source not found')

    def _save_text_file(self, path: Path, data: str) -> None:
        with open(path, 'w', encoding='utf-8') as f_target:
            f_target.write(data)


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
        project_data_len = len(ProjectData._fields)
        try:
            with open(PROJECT_FILE, 'r') as f_projects:
                raw_data = json.load(f_projects)
                for data in raw_data:
                    data = data + ['' for _ in range(project_data_len)]
                    data = data[:project_data_len]
                    project = Project(ProjectData(*data))
                    projects[project.name] = project
        except FileNotFoundError:
            print(f'*** {PROJECT_FILE} FileNotFoundError ***')
            return []
        except IsADirectoryError:
            print(f'*** {PROJECT_FILE} IsADirectoryError ***')
            return []
        except json.decoder.JSONDecodeError:
            print(f'*** {PROJECT_FILE} SONDecodeError ***')
            return []
        return projects

    def save_projects(self, projects: list[Project] = None) -> None:
        try:
            os.makedirs(USER_DATA_DIR)
        except FileExistsError:
            pass
        if not projects:
            projects = self.projects
        projects = [project.serialize() for project in projects.values()]
        with open(PROJECT_FILE, 'w') as f_projects:
            json.dump(projects, f_projects)
