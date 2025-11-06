import shutil
from pathlib import Path
import subprocess

from psiconfig import TomlConfig

from windows_converter import logger


def build_project(
        project: object,
        config: TomlConfig,
        windows_projects_dir: str,
        update_requirements: bool = False,
        testing: bool = False,
        ) -> None:
    """Create the project in windows-projects."""
    del testing
    windows_project_dir = Path(
        config.windows_base_directory, windows_projects_dir)
    code_dir = Path(windows_project_dir, 'src')
    target = Path(windows_project_dir).parts[-1]

    logger.info((f'Start building {project.project_base_dir} '
                 f'to {target}'))

    # Remove old project
    if windows_project_dir.is_dir():
        shutil.rmtree(windows_project_dir)
    logger.info('Old project data removed')

    _create_directories(project, windows_project_dir, code_dir)
    _create_tests_directory(project, windows_project_dir)
    _create_pyinstaller(project, code_dir)
    _create_pyproject(project, windows_project_dir)
    _create_readme(windows_project_dir)
    _create_installforge(project, windows_project_dir)
    _create_copy_requirements(project, code_dir, update_requirements)
    logger.info('Build complete')
    return project.status_ok


def _create_directories(
        project, windows_project_dir: Path, code_dir: Path) -> None:
    # Create project directory
    windows_project_dir.mkdir(parents=True, exist_ok=True)
    logger.info(f'Created windows project dir {windows_project_dir}')

    # Create the code directory
    code_dir.mkdir(parents=True, exist_ok=True)
    logger.info(f'Created code dir {code_dir}')

    # Create the setup directory
    setup_dir = Path(windows_project_dir, 'setup')
    setup_dir.mkdir(parents=True, exist_ok=True)
    logger.info(f'Created setup dir {setup_dir}')

    # Build src directory
    src_dir = Path(code_dir, project.windows_projects_dir)
    shutil.copytree(project.src_directory, src_dir, dirs_exist_ok=True)
    logger.info(f'Source copied to {src_dir}')


def _create_tests_directory(project, windows_project_dir: Path) -> None:
    tests_dir = Path(windows_project_dir, 'tests')
    tests_dir.mkdir(parents=True, exist_ok=True)
    if project.tests_directory:
        shutil.copytree(
            project.tests_directory, tests_dir, dirs_exist_ok=True)
    logger.info(f'Created tests dir {tests_dir}')


def _create_pyinstaller(project, code_dir: Path) -> None:
    file_name = 'pyinstaller.py'
    code = _get_text_file(file_name)
    code = code.replace('<exe_name>', project.exe_name)
    code = code.replace('<project>', project.name)
    target_file = Path(code_dir, file_name)
    _save_text_file(target_file, code)
    logger.info(f'Created {file_name}')


def _create_pyproject(project, windows_project_dir: Path) -> None:
    file_name = 'pyproject.toml'
    code = _get_text_file(file_name)
    code = code.replace('<description>', project.description)
    code = code.replace('<author>', project.author)
    code = code.replace('<email>', project.email)
    code = code.replace('<project>', project.name)
    code = code.replace('<project_dir>', project.windows_projects_dir)
    code = code.replace('<version>', project.version)
    target_file = Path(windows_project_dir, file_name)
    _save_text_file(target_file, code)
    logger.info(f'Created {file_name}')


def _create_readme(windows_project_dir: Path) -> None:
    file_name = 'README.md'
    code = ''
    target_file = Path(windows_project_dir, file_name)
    _save_text_file(target_file, code)
    logger.info(f'Created {file_name}')


def _create_installforge(project, windows_project_dir: Path) -> None:
    file_name = 'installforge.ifp'
    code = _get_text_file(file_name)
    code = code.replace('<<name>>', project.description)
    code = code.replace('<<company name>>', project.company_name)
    code = code.replace('<<windows directory>>', project.windows_directory)
    code = code.replace('<<exe name>>', project.exe_name)
    code = code.replace('<<installation path>>', project.installation_path)
    code = code.replace('<<version>>', project.version)
    code = code.replace('<<start menu text>>', project.start_menu_text)
    target_file = Path(windows_project_dir, f'{project.name}.ifp')
    _save_text_file(target_file, code)
    logger.info(f'Created {file_name}')


def _create_copy_requirements(
        project, code_dir: Path, update_requirements: bool) -> None:
    if update_requirements:
        _create_requirements(project)
    _copy_requirements(project, code_dir)


def _create_requirements(project) -> int:

    # Use the venv's python to run pip
    # ensure pip is installed
    command = [project.project_base_dir, '-m', 'ensurepip', '--upgrade']

    with open(
            Path(project.project_base_dir, 'requirements.txt'),
            'w',
            encoding='utf-8') as f_requirements:
        subprocess.run(
            [
                f'{project.project_base_dir}/.venv/bin/pip',
                'freeze',
                '--exclude-editable',
            ],
            stdout=f_requirements,
            check=True
        )
        logger.info(
            "Update project dependencies"
        )


def _copy_requirements(project, code_dir: Path) -> None:
    file_name = 'requirements.txt'
    requirements_source = Path(
        Path(project.project_base_dir), file_name)
    if requirements_source.is_file():
        requirements_target = Path(
            Path(code_dir).parent, file_name)
        shutil.copyfile(requirements_source, requirements_target)
        logger.info(f'Created {file_name}')
    else:
        logger.warning(f'No {file_name} in project source directory')


def _get_text_file(file_name: str) -> str:
    src_file = Path(Path(__file__).parent.parent, 'data', file_name)
    try:
        with open(src_file, 'r', encoding='utf-8') as f_source:
            return f_source.read()
    except FileNotFoundError:
        print(f'{src_file} source not found')


def _save_text_file(path: Path, data: str) -> None:
    with open(path, 'w', encoding='utf-8') as f_target:
        f_target.write(data)
