import os
import shutil
from pathlib import Path
import subprocess

from psiconfig import TomlConfig
from psiutils.constants import Status

from windows_converter import logger


def build_project(
        project: object,
        config: TomlConfig,
        update_requirements: bool = False,
        testing: bool = False,
        ) -> None:
    """Create the project in windows-projects."""
    del testing
    build_project_dir = Path(
        config.build_base_dir, project.name)
    build_src_dir = Path(build_project_dir, 'src')
    target = Path(build_project_dir).parts[-1]

    logger.info((f'Start building {project.dev_base_dir} '
                 f'to {target}'))

    # Remove old project
    if build_project_dir.is_dir():
        shutil.rmtree(build_project_dir)
    logger.info('Old project data removed')

    _create_directories(project, build_project_dir, build_src_dir)
    _create_tests_directory(project, build_project_dir)
    _create_build_file(project, build_src_dir, 'pyinstaller.py')
    _create_build_file(project, build_src_dir, 'pyinstaller_backend.py')
    _create_build_file(project, Path(
        build_src_dir, Path(project.dev_source_dir).parts[-1]), 'build_exe.py')
    _create_build_file(project, build_project_dir, 'pyproject.toml')
    _create_build_file(project, build_project_dir, 'justfile')
    _create_readme(build_project_dir)
    _create_installforge(project, build_project_dir)
    _create_copy_requirements(project, build_src_dir, update_requirements)
    logger.info('Build complete')
    return project.status_ok


def _create_directories(
        project, build_project_dir: Path, build_src_dir: Path) -> None:
    # Create project directory
    build_project_dir.mkdir(parents=True, exist_ok=True)
    logger.info(f'Created windows project dir {build_project_dir}')

    # Create the code directory
    build_src_dir.mkdir(parents=True, exist_ok=True)
    logger.info(f'Created code dir {build_src_dir}')

    # Create the setup directory
    setup_dir = Path(build_project_dir, 'setup')
    setup_dir.mkdir(parents=True, exist_ok=True)
    logger.info(f'Created setup dir {setup_dir}')

    # Build src directory
    src_dir = Path(build_src_dir, project.name)
    shutil.copytree(project.dev_source_dir, src_dir, dirs_exist_ok=True)
    logger.info(f'Source copied to {src_dir}')


def _create_tests_directory(project, build_project_dir: Path) -> None:
    tests_dir = Path(build_project_dir, 'tests')
    tests_dir.mkdir(parents=True, exist_ok=True)
    if project.tests_directory:
        shutil.copytree(
            project.tests_directory, tests_dir, dirs_exist_ok=True)
    logger.info(f'Created tests dir {tests_dir}')


def _create_build_file(project, target_dir: Path, file_name: str) -> None:
    code = _get_text_file(file_name)
    code = code.replace('<exe_name>', project.exe_name)
    code = code.replace('<project>', project.name)
    code = code.replace('<description>', project.description)
    code = code.replace('<author>', project.author)
    code = code.replace('<email>', project.email)
    code = code.replace('<project>', project.name)
    # code = code.replace('<project_dir>', project.win_base_dir)
    code = code.replace('<version>', project.version)
    # code = code.replace('<win_base_dir>', project.win_source_dir)
    target_file = Path(target_dir, file_name)
    _save_text_file(target_file, code)
    logger.info(f'Created {file_name}')


def _create_readme(build_project_dir: Path) -> None:
    file_name = 'README.md'
    code = ''
    target_file = Path(build_project_dir, file_name)
    _save_text_file(target_file, code)
    logger.info(f'Created {file_name}')


def _create_installforge(project, build_project_dir: Path) -> None:
    file_name = 'installforge.ifp'
    code = _get_text_file(file_name)
    code = code.replace('<<name>>', project.description)
    code = code.replace('<<company name>>', project.company_name)
    code = code.replace('<<windows directory>>', project.win_source_dir)
    code = code.replace('<<exe name>>', project.exe_name)
    code = code.replace('<<installation path>>', project.win_install_path)
    code = code.replace('<<version>>', project.version)
    code = code.replace('<<start menu text>>', project.start_menu_text)
    target_file = Path(build_project_dir, f'{project.name}.ifp')
    _save_text_file(target_file, code)
    logger.info(f'Created {file_name}')


def _create_copy_requirements(
        project, build_src_dir: Path, update_requirements: bool) -> None:
    if update_requirements:
        _create_requirements(project)
    _copy_requirements(project, build_src_dir)


def _create_requirements(project) -> int:
    venv_python = Path(project.dev_base_dir, '.venv', 'bin', 'python')
    req_path = Path(project.dev_base_dir, 'requirements.txt')

    try:
        subprocess.run(
            [venv_python, '-m', 'ensurepip', '--upgrade'],
            check=True,
            capture_output=True)
    except subprocess.CalledProcessError:
        return Status.ERROR

    try:
        freeze = subprocess.run(
            ['uv', 'pip', 'freeze', '--exclude-editable'],
            capture_output=True,
            text=True,
            check=True,
            cwd=project.dev_base_dir
        )
        lines = [line for line in freeze.stdout.splitlines()
                 if not line.startswith('pygobject')]
        req_path.write_text('\n'.join(lines) + '\n')
        logger.info(
            "Updated project dependencies"
        )
        return Status.OK
    except Exception as e:
        logger.warning(f'{req_path} not created', Exception=f'{e}')
        return Status.ERROR


def _copy_requirements(project, build_src_dir: Path) -> None:
    file_name = 'requirements.txt'
    requirements_source = Path(
        Path(project.dev_base_dir), file_name)
    if requirements_source.is_file():
        requirements_target = Path(
            Path(build_src_dir).parent, file_name)
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
        logger.warning(f'{src_file} source not found')
        return ''


def _save_text_file(path: Path, data: str) -> None:
    with open(path, 'w', encoding='utf-8') as f_target:
        f_target.write(data)
