"""Project tests for Windows app converter"""

from pathlib import Path

from projects import ProjectsAgent
from config import read_config

parent = Path(__file__).parent
CONFIG_FILE = Path(parent, 'test_data', 'config.toml')

config = read_config(CONFIG_FILE)
project_file = Path(config.data_directory, 'projects.json')
projects = ProjectsAgent(project_file).projects
for project in projects:
    if project.name == 'minimal-app':
        min_project = project
        break

min_project.build(config, testing=True)
WINDOWS_PROJECT_DIR = Path(
    config.build_base_dir, min_project.directory)
CODE_DIR = Path(WINDOWS_PROJECT_DIR, min_project.directory)

IFP_PROJECT = Path(WINDOWS_PROJECT_DIR, 'minimal-app.ifp')
IFP_PROOF = Path(parent, 'test_data', 'minimal-app_proof.ifp')

PY_INST_PROJECT = Path(WINDOWS_PROJECT_DIR, 'py_installer.py')
PY_INST_PROOF = Path(parent, 'test_data', 'py_installer_proof.py')

PYPROJECT_PROJECT = Path(WINDOWS_PROJECT_DIR, 'pyproject.toml')
PYPROJECT_PROOF = Path(parent, 'test_data', 'pyproject_proof.toml')


def _read_text_file(src_file) -> str:
    try:
        with open(src_file, encoding="utf8", errors='ignore') as f_source:
            return f_source.read()
    except FileNotFoundError:
        print(f'{src_file} source not found')


def test_is_working():
    assert True


def test_config():
    data_directory = str(Path(parent, 'test_data'))
    windows_home = str(Path(parent, 'test_data', 'windows-projects'))
    assert config.data_directory == data_directory
    assert config.build_base_dir == windows_home


def test_number_of_projects():
    assert len(projects) == 2


def test_project_attributes():
    print(min_project.dev_source_dir)
    assert min_project.name == 'minimal-app'
    assert min_project.win_install_path == 'BfG\\MinimalApp'
    assert min_project.exe_name == 'MinimalApp'


def test_files_created():
    assert WINDOWS_PROJECT_DIR.is_dir()
    assert CODE_DIR.is_dir()

    assert Path(WINDOWS_PROJECT_DIR, 'pyproject.toml').is_file()
    assert Path(IFP_PROJECT).is_file()
    assert Path(CODE_DIR, 'pyinstaller.py').is_file()


def test_install_forge_file():
    ifp_proof_text = _read_text_file(IFP_PROOF)
    ifp_project_text = _read_text_file(IFP_PROJECT)
    assert ifp_proof_text == ifp_project_text


def test_pyinstaller_file():
    py_installer_proof_text = _read_text_file(PY_INST_PROOF)
    py_installer_text = _read_text_file(PY_INST_PROJECT)
    assert py_installer_proof_text == py_installer_text


def test_pyproject_file():
    pyproject_proof_text = _read_text_file(PYPROJECT_PROOF)
    pyproject_text = _read_text_file(PYPROJECT_PROJECT)
    assert pyproject_proof_text == pyproject_text
