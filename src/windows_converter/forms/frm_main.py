
"""MainFrame for Windows converter."""
import tkinter as tk
from tkinter import ttk
from pathlib import Path

from psiutils.constants import PAD, MODES
from psiutils.buttons import ButtonFrame
from psiutils.widgets import HAND
from psiutils.utilities import window_resize
from psiutils.menus import Menu, MenuItem


from windows_converter.config import read_config
from windows_converter.projects import ProjectServer
from windows_converter.constants import APP_TITLE
from windows_converter.text import Text

from windows_converter.main_menu import MainMenu
from windows_converter.forms.frm_project import ProjectFrame

txt = Text(1)
FRAME_TITLE = APP_TITLE


class MainFrame():
    def __init__(self, root: tk.Tk) -> None:
        # pylint: disable=no-member)
        self.root = root
        self.project_server = ProjectServer()
        self.projects = self.project_server.projects
        self.project = None
        self.config = read_config()
        self.listbox = None

        # tk variables
        self.project_name = tk.StringVar()
        self.project_list = tk.StringVar(value=sorted(list(self.projects)))

        self.context_menu = self._context_menu()
        self._show()

        last_project = self.config.last_project
        if last_project and last_project in self.projects:
            index = sorted(list(self.projects)).index(last_project)
            self.listbox.select_set(index)
            self._project_selected(last_project)

    def _show(self):
        # pylint: disable=no-member)
        root = self.root
        root.geometry(self.config.geometry[Path(__file__).stem])
        root.title(FRAME_TITLE)

        root.bind('<Control-x>', self._dismiss)
        root.bind('<Control-n>', self._new_project)
        root.bind('<Control-b>', self._build_project)
        root.bind('<Configure>',
                  lambda e: window_resize(self, __file__))

        main_menu = MainMenu(self)
        main_menu.create()

        root.rowconfigure(0, weight=1)
        root.columnconfigure(0, weight=1)

        main_frame = self._main_frame(root)
        main_frame.grid(row=0, column=0, sticky=tk.NSEW, padx=PAD, pady=PAD)

        self.button_frame = self._button_frame(root)
        self.button_frame.grid(row=0, column=1,
                               sticky=tk.NS, padx=PAD, pady=PAD)

        sizegrip = ttk.Sizegrip(root)
        sizegrip.grid(column=2, sticky=tk.SE)

    def _main_frame(self, master: tk.Frame) -> ttk.Frame:
        frame = ttk.Frame(master)
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)
        self.listbox = tk.Listbox(
            frame,
            listvariable=self.project_list,
            height=6,
            selectmode=tk.BROWSE,
            cursor=HAND,
        )
        self.listbox.grid(row=0, column=0, sticky=tk.NSEW, padx=PAD)
        self.listbox.bind('<<ListboxSelect>>', self._project_clicked)
        self.listbox.bind('<Button-3>', self._show_context_menu)

        return frame

    def _button_frame(self, master: tk.Frame) -> tk.Frame:
        frame = ttk.Frame(master)
        frame = ButtonFrame(master, tk.VERTICAL)
        frame.buttons = [
            frame.icon_button('new', False, self._new_project),
            frame.icon_button('build', True, self._build_project),
            frame.icon_button('close', False, self._dismiss),
        ]
        frame.enable(False)
        return frame

    def _show_context_menu(self, event) -> None:
        self.context_menu.tk_popup(event.x_root, event.y_root)
        self.listbox.selection_clear(0, tk.END)
        self.listbox.selection_set(self.listbox.nearest(event.y))
        self._project_clicked(event)

    def _context_menu(self) -> tk.Menu:
        # pylint: disable=no-member)
        menu_items = [
            MenuItem(txt.NEW, self._new_project),
            MenuItem(txt.BUILD, self._build_project, dimmable=True),
        ]
        context_menu = Menu(self.root, menu_items)
        context_menu.enable(False)
        return context_menu

    def _project_clicked(self, event: tk.Event) -> None:
        self.button_frame.disable()
        selection = event.widget.curselection()
        if not selection:
            return
        names = sorted(list(self.projects))
        self._project_selected(names[selection[0]])
        self.config.update('last_project', self.project.name)
        self.config.save()

    def _project_selected(self, project_name: str) -> None:
        self.project = self.projects[project_name]
        self.button_frame.enable()
        self.context_menu.enable()

    def _new_project(self, *args) -> None:
        dlg = ProjectFrame(self, MODES['new'])
        self.root.wait_window(dlg.root)

        if dlg.project.name and dlg.project:
            self.projects[dlg.project.name] = dlg.project
            self.project_list.set(sorted(list(self.projects)))

    def _build_project(self, *args) -> None:
        dlg = ProjectFrame(self, MODES['edit'], self.project)
        self.root.wait_window(dlg.root)

    def _dismiss(self, *args) -> None:
        self.root.destroy()
