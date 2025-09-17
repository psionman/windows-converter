import tkinter as tk
from tkinter import messagebox
import webbrowser

from psiutils.menus import Menu, MenuItem

from windows_converter.constants import AUTHOR, APP_TITLE, HELP_URI
from windows_converter._version import __version__
from windows_converter.text import Text
from windows_converter.config import config

from windows_converter.forms.frm_config import ConfigFrame

txt = Text()
SPACES = ' '*20


class MainMenu():
    def __init__(self, parent):
        self.parent = parent
        self.root = parent.root

    def create(self):
        menubar = tk.Menu()
        self.root['menu'] = menubar

        # File menu
        file_menu = Menu(menubar, self._file_menu_items())
        menubar.add_cascade(menu=file_menu, label='File')

        # Help menu
        help_menu = Menu(menubar, self._help_menu_items())
        menubar.add_cascade(menu=help_menu, label='Help')

    def _file_menu_items(self) -> list:
        # pylint: disable=no-member)
        return [
            MenuItem(f'{txt.CONFIG}{txt.ELLIPSIS}', self._show_config_frame),
            MenuItem(txt.EXIT, self._dismiss),
        ]

    def _show_config_frame(self):
        """Display the config frame."""
        dlg = ConfigFrame(self)
        self.root.wait_window(dlg.root)

    def _help_menu_items(self) -> list:
        # pylint: disable=no-member)
        return [
            MenuItem(f'On line help{txt.ELLIPSIS}', self._show_help),
            MenuItem(f'Data directory location{txt.ELLIPSIS}',
                     self._show_data_directory),
            MenuItem(f'About{txt.ELLIPSIS}', self._show_about),
        ]

    def _show_help(self):
        webbrowser.open(HELP_URI)

    def _show_data_directory(self):
        # pylint: disable=no-member)
        data_dir = f'Data directory: {config.data_directory} {SPACES}'
        messagebox.showinfo(title='Data directory', message=data_dir)

    def _show_about(self):
        about = (f'{APP_TITLE}\n'
                 f'Version: {__version__}\n'
                 f'Author: {AUTHOR} {SPACES}')
        messagebox.showinfo(title=f'About {APP_TITLE}', message=about)

    def _dismiss(self, *args):
        self.root.destroy()
