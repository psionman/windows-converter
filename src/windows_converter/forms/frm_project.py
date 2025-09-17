
"""ProjectFrame for Windows converter."""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import re

from psiutils.constants import PAD, MODES
from psiutils.buttons import ButtonFrame
from psiutils.widgets import separator_frame, Tooltip
from psiutils.utilities import window_resize

from windows_converter.constants import APP_TITLE
from windows_converter.config import read_config
from windows_converter.projects import Project
from windows_converter.text import Text

txt = Text()
FRAME_TITLE = f'{APP_TITLE} - MODE project'


class ProjectFrame():
    def __init__(self, parent: tk.Frame,
                 mode: int, project: Project = None) -> None:
        # pylint: disable=no-member)
        self.root = tk.Toplevel(parent.root)
        self.parent = parent
        self.config = read_config()
        self.mode = mode
        self.project_server = parent.project_server
        if not project:
            project = Project()
            project.author = self.config.author
        self.project = project
        dev_dir_tooltip = f'e.g. /home/jeff/projects/{project.name}/src'
        source_dir_tooltip = (f'e.g. /home/jeff/projects/{project.name}'
                              f'/src/{project.name}')
        image_dir_tooltip = (f'e.g. /home/jeff/projects/{project.name}'
                             f'/src/images')

        # tk variables
        self.project_name = tk.StringVar(value=self.project.name)
        self.description = tk.StringVar(value=self.project.description)
        self.author = tk.StringVar(value=self.project.author)
        self.exe_name = tk.StringVar(value=self.project.exe_name)
        self.windows_projects_directory = tk.StringVar(
            value=self.project.windows_projects_directory)

        self.project_development_directory = tk.StringVar(
            value=self.project.project_development_directory)
        self.development_directory_tooltip_text = tk.StringVar(
            value=dev_dir_tooltip)

        self.source_directory = tk.StringVar(
            value=self.project.src_directory)
        self.source_directory_tooltip_text = tk.StringVar(
            value=source_dir_tooltip)

        self.image_directory = tk.StringVar(
            value=self.project.image_directory)
        self.image_directory_tooltip_text = tk.StringVar(
            value=image_dir_tooltip)

        self.windows_directory = tk.StringVar(
            value=self.project.windows_directory)
        self.company_name = tk.StringVar(value=self.project.company_name)
        self.installation_path = tk.StringVar(
            value=self.project.installation_path)
        self.start_menu_text = tk.StringVar(value=self.project.start_menu_text)
        self.version = tk.StringVar(value=self.project.version)
        self.close_on_build = tk.BooleanVar(value=True)

        self.project_name.trace_add('write', self._project_name_changed)
        self.company_name.trace_add('write', self._company_name_changed)

        self._show()
        self._source_directory_changed()

    def _show(self) -> None:
        # pylint: disable=no-member)
        root = self.root
        root.geometry(self.config.geometry[Path(__file__).stem])
        root.transient(self.parent.root)
        root.title(FRAME_TITLE.replace('MODE', MODES[self.mode]))

        root.bind('<Control-x>', self._dismiss)
        root.bind('<Control-s>', self._save_project)
        root.bind('<Control-b>', self._build)
        root.bind('<Configure>',
                  lambda e: window_resize(self, __file__))

        root.rowconfigure(0, weight=1)
        root.columnconfigure(0, weight=1)

        main_frame = self._main_frame(root)
        main_frame.grid(row=0, column=0, sticky=tk.NSEW, padx=PAD)
        self.button_frame = self._button_frame(root)
        self.button_frame.grid(row=8, column=0, columnspan=9,
                               sticky=tk.EW, padx=PAD)

        sizegrip = ttk.Sizegrip(root)
        sizegrip.grid(sticky=tk.SE)

    def _main_frame(self, master: tk.Frame) -> ttk.Frame:
        # pylint: disable=no-member)
        frame = ttk.Frame(master)
        frame.columnconfigure(1, weight=1)

        row = 0
        # Project name
        label = ttk.Label(frame, text='Project name')
        label.grid(row=0, column=0, sticky=tk.E, padx=PAD, pady=PAD)
        entry = ttk.Entry(frame, textvariable=self.project_name)
        entry.grid(row=0, column=1, sticky=tk.EW, pady=PAD)
        if self.mode == MODES['new']:
            entry.focus_set()
        else:
            entry.configure(state='disable')

        row += 1
        # Windows project dir
        label = ttk.Label(frame, text='Directory in windows-projects')
        label.grid(row=row, column=0, sticky=tk.E, padx=PAD, pady=PAD)
        entry = ttk.Entry(frame, textvariable=self.windows_projects_directory)
        entry.grid(row=row, column=1, sticky=tk.EW)

        row += 1
        # Description
        label = ttk.Label(frame, text='Description')
        label.grid(row=row, column=0, sticky=tk.E, padx=PAD, pady=PAD)
        entry = ttk.Entry(frame, textvariable=self.description)
        entry.grid(row=row, column=1, sticky=tk.EW)

        row += 1
        # Author
        label = ttk.Label(frame, text='Author')
        label.grid(row=row, column=0, sticky=tk.E, padx=PAD, pady=PAD)
        entry = ttk.Entry(frame, textvariable=self.author)
        entry.grid(row=row, column=1, sticky=tk.EW)

        row += 1
        # Exe name
        label = ttk.Label(frame, text='Exe name')
        label.grid(row=row, column=0, sticky=tk.E, padx=PAD, pady=PAD)
        entry = ttk.Entry(frame, textvariable=self.exe_name)
        entry.grid(row=row, column=1, sticky=tk.EW)

        row += 1
        # Version
        label = ttk.Label(frame, text='Version')
        label.grid(row=row, column=0, sticky=tk.E, padx=PAD, pady=PAD)
        entry = ttk.Entry(frame, textvariable=self.version)
        entry.grid(row=row, column=1, sticky=tk.EW)

        row += 1
        # LOcal dirs
        separator = separator_frame(frame, 'Local directories')
        separator.grid(row=row, column=0, columnspan=4,
                       sticky=tk.EW, padx=PAD)

        row += 1
        # Project dir
        label = ttk.Label(frame, text='Project directory')
        label.grid(row=row, column=0, sticky=tk.E, padx=PAD, pady=PAD)
        entry = ttk.Entry(
            frame, textvariable=self.project_development_directory)
        entry.grid(row=row, column=1, sticky=tk.EW)
        self._entry_tooltip(entry, self.development_directory_tooltip_text,)
        button = ttk.Button(frame, text=txt.ELLIPSIS,
                            command=self._project_directory)
        button.grid(row=row, column=3, padx=PAD)

        row += 1
        # Source dir
        label = ttk.Label(frame, text='Source directory')
        label.grid(row=row, column=0, sticky=tk.E, padx=PAD, pady=PAD)
        entry = ttk.Entry(frame, textvariable=self.source_directory)
        entry.grid(row=row, column=1, sticky=tk.EW)
        self._entry_tooltip(entry, self.source_directory_tooltip_text,)
        button = ttk.Button(frame, text=txt.ELLIPSIS,
                            command=self._source_directory)
        button.grid(row=row, column=3, padx=PAD)

        row += 1
        # Images dir
        label = ttk.Label(frame, text='Images directory')
        label.grid(row=row, column=0, sticky=tk.E, padx=PAD, pady=PAD)
        entry = ttk.Entry(frame, textvariable=self.image_directory)
        entry.grid(row=row, column=1, sticky=tk.EW)
        self._entry_tooltip(entry, self.image_directory_tooltip_text,)
        button = ttk.Button(frame, text=txt.ELLIPSIS,
                            command=self._image_directory)
        button.grid(row=row, column=3, padx=PAD)

        row += 1
        separator = separator_frame(frame, 'Windows')
        separator.grid(row=row, column=0, columnspan=4,
                       sticky=tk.EW, padx=PAD)

        row += 1
        # Company name
        label = ttk.Label(frame, text='Company name')
        label.grid(row=row, column=0, sticky=tk.E, padx=PAD, pady=PAD)
        entry = ttk.Entry(frame, textvariable=self.company_name)
        entry.grid(row=row, column=1, sticky=tk.EW)

        row += 1
        # Windows project dir
        label = ttk.Label(frame, text='Windows project directory')
        label.grid(row=row, column=0, sticky=tk.E, padx=PAD, pady=PAD)
        entry = ttk.Entry(frame, textvariable=self.windows_directory)
        entry.grid(row=row, column=1, sticky=tk.EW)

        row += 1
        # Installation path
        label = ttk.Label(frame, text='Installation path')
        label.grid(row=row, column=0, sticky=tk.E, padx=PAD, pady=PAD)
        entry = ttk.Entry(frame, textvariable=self.installation_path)
        entry.grid(row=row, column=1, sticky=tk.EW)

        row += 1
        # Start menu text
        label = ttk.Label(frame, text='Start menu text')
        label.grid(row=row, column=0, sticky=tk.E, padx=PAD, pady=PAD)
        entry = ttk.Entry(frame, textvariable=self.start_menu_text)
        entry.grid(row=row, column=1, sticky=tk.EW)

        row += 1
        separator = separator_frame(frame, 'Build')
        separator.grid(row=row, column=0, columnspan=4,
                       sticky=tk.EW, padx=PAD)

        row += 1
        # Close after build
        check_button = tk.Checkbutton(frame, text='Close after build',
                                      variable=self.close_on_build)
        check_button.grid(row=row, column=1, sticky=tk.W)

        return frame

    def _button_frame(self, master: tk.Frame) -> tk.Frame:
        frame = ButtonFrame(master, tk.HORIZONTAL)
        frame.buttons = [
            frame.icon_button('save', False, self._save_project),
            frame.icon_button('build', False, self._build),
            frame.icon_button('exit', False, self._dismiss),
        ]
        frame.enable(False)
        return frame

    def _entry_tooltip(self, entry: ttk.Entry, tk_var: tk.StringVar) -> None:
        entry.tooltip = Tooltip(entry, textvariable=tk_var, wrap_length=2000)
        entry.bind('<Enter>', entry.tooltip.onEnter)
        entry.bind('<Leave>', entry.tooltip.onLeave)

    def _project_directory(self, *args) -> None:
        # pylint: disable=no-member)
        initialdir = self.project_development_directory.get()
        if not initialdir:
            initialdir = self.config.projects_directory
        dlg = filedialog.askdirectory(
            initialdir=initialdir,
        )
        if dlg:
            self.project_development_directory.set(dlg)

    def _source_directory(self, *args) -> None:
        dlg = filedialog.askdirectory(
            initialdir=self.project_development_directory.get(),
        )
        if dlg:
            self.source_directory.set(dlg)

    def _image_directory(self, *args) -> None:
        dlg = filedialog.askdirectory(
            initialdir=self.project_development_directory.get(),
        )
        if dlg:
            self.image_directory.set(dlg)
            self._source_directory_changed()

    def _source_directory_changed(self) -> None:
        if not self.source_directory.get():
            return
        try:
            src_dir = Path(self.source_directory.get(), '_version.py')
            with open(src_dir, 'r', encoding='utf-8') as f_version:
                version = f_version.read()

                version_re = r'[0-9]{1,}.[0-9]{1,}.[0-9]{1,}'
                match = re.search(version_re, version)
                if not match:
                    print('*** Invalid _version.py file structure ***')
                    return
                self.version.set(match.group())

        except FileNotFoundError:
            messagebox.showwarning(
                '',
                'No _version file found'
            )

    def _project_name_changed(self, *args) -> None:
        # pylint: disable=no-member)
        if self.mode != MODES['new']:
            return

        name = self.project_name.get()
        self.description.set(self._name_upper(name))
        self.windows_projects_directory.set(name)
        self.exe_name.set(self._name_upper(name, delimiter=''))
        self.start_menu_text.set(self.description.get())
        self.installation_path.set(
            f'{self.config.windows_project_directory}\\{name}'
        )
        self.windows_directory.set(
            f'{self.config.windows_project_directory}\\{name}'
        )
        self.installation_path.set(
            f'{self.company_name.get()}\\{self.exe_name.get()}'
        )

    def _company_name_changed(self, *args) -> None:
        if self.company_name.get():
            self.installation_path.set(
                f'\\{self.company_name.get()}\\{self.exe_name.get()}'
            )
        else:
            self.installation_path.set(
                f'\\{self.exe_name.get()}'
            )

    def _name_contract(self, name: str, delimiter: str = '') -> str:
        words = name.split('_')
        upper = [word.capitalize() for word in words]
        return delimiter.join(upper)

    def _name_upper(self, name: str, delimiter: str = ' ') -> str:
        name = name.replace('_', ' ')
        words = name.split(' ')
        upper = [word.capitalize() for word in words]
        return delimiter.join(upper)

    def _save_project(self, *args) -> None:
        if not self._check_spaces_in_name():
            return

        if self.mode == MODES['new']:
            self.project = Project()

        self.project.name = self.project_name.get()
        self.project.description = self.description.get()
        self.project.author = self.author.get()
        self.project.exe_name = self.exe_name.get()
        windows_projects_directory = self.windows_projects_directory.get()
        self.project.windows_projects_directory = windows_projects_directory
        project_development_dir = self.project_development_directory.get()
        self.project.project_development_directory = project_development_dir
        self.project.src_directory = self.source_directory.get()
        self.project.image_directory = self.image_directory.get()
        self.project.windows_directory = self.windows_directory.get()
        self.project.company_name = self.company_name.get()
        self.project.installation_path = self.installation_path.get()
        self.project.start_menu_text = self.start_menu_text.get()
        self.project.version = self.version.get()

        self.project_server.projects[self.project.name] = self.project
        self.project_server.save_projects()

    def _check_spaces_in_name(self) -> bool:
        if ' ' not in self.project_name.get():
            return True

        dlg = messagebox.askyesno(
            '',
            'There are spaces in the project name. Is this correct?',
            parent=self.root,
        )
        if dlg:
            return True
        return False

    def _build(self, *args) -> None:
        if not self._check_spaces_in_name():
            return

        config = read_config()
        self._update_project()
        result = self.project.build(config)
        if result == self.project.status_ok:
            messagebox.showinfo(
                '',
                'Build_complete'
            )
            if self.close_on_build.get():
                self._dismiss()
        else:
            messagebox.showerror(
                '',
                'Build failed!'
            )

    def _update_project(self) -> None:
        self.project.description = self.description.get()
        self.project.author = self.author.get()
        self.project.exe_name = self.exe_name.get()
        windows_projects_directory = self.windows_projects_directory.get()
        self.project.windows_projects_directory = windows_projects_directory
        project_development_dir = self.project_development_directory.get()
        self.project.project_development_directory = project_development_dir
        self.project.src_directory = self.source_directory.get()
        self.project.image_directory = self.image_directory.get()
        self.project.windows_directory = self.windows_directory.get()
        self.project.company_name = self.company_name.get()
        self.project.installation_path = self.installation_path.get()
        self.project.start_menu_text = self.start_menu_text.get()
        self.project.version = self.version.get()

    def _dismiss(self, *args) -> None:
        self.root.destroy()
