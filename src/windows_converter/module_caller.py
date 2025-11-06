import sys

from psiutils.constants import MODES
from psiutils.utilities import notify

from windows_converter.config import read_config
from windows_converter.projects import ProjectServer

from windows_converter.forms.frm_config import ConfigFrame
from windows_converter.forms.frm_project import ProjectFrame

class ModuleCaller():
    def __init__(self, root, module) -> None:
        modules = {
            'config': self._config,
            'project': self._project
            }
        self.config = None
        self.project_server = None

        self.invalid = False
        if module == '-h':
            for key in sorted(list(modules.keys())+['main']):
                print(key)
            self.invalid = True
            return

        if module not in modules:
            if module != 'main':
                print(f'Invalid function name: {module}')
            self.invalid = True
            return

        self.root = root
        modules[module]()
        self.root.destroy()
        return

    def _config(self) -> None:
        dlg = ConfigFrame(self)
        self.root.wait_window(dlg.root)

    def _project(self) -> None:
        self.config = read_config()
        self.project_server = ProjectServer()
        projects = self.project_server.read_projects()
        item = 0
        if len(sys.argv) > 2:
            item = sys.argv[2]
            if item not in projects:
                msg =f'*** {item} not in Windows Builder\'s projects ***'
                print(msg)
                notify('Windows Builder', msg)
                return
            dlg = ProjectFrame(self, MODES['edit'], projects[item])
        else:
            dlg = ProjectFrame(self, MODES['new'])
        self.root.wait_window(dlg.root)
