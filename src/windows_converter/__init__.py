"""Initialise the application."""
from psiutils.utilities import psi_logger
from windows_converter.constants import APP_NAME

logger = psi_logger(APP_NAME)



#     pip_path = Path(project.dev_base_dir, '.venv', 'bin', 'pip')

#     with open(req_path, 'w', encoding='utf-8') as f:
#         subprocess.run([pip_path, 'freeze', '--exclude-editable'], stdout=f, check=True)

#         ic| build.py:167 in _create_requirements() at 08:48:37.848
# ic| build.py:171 in _create_requirements()
#     req_path: PosixPath('/home/jeff/projects/phoenix/programs/directors_rota/requirements.txt')
# ic| build.py:172 in _create_requirements()
#     e: FileNotFoundError(2, 'No such file or directory')
