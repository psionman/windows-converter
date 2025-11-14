
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
from windows_converter import logger

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
        self.project_id = tk.StringVar(value=self.project.name)
        self.description = tk.StringVar(value=self.project.description)
        self.author = tk.StringVar(value=self.project.author)
        self.email = tk.StringVar(value=self.project.email)
        self.exe_name = tk.StringVar(value=self.project.exe_name)
        self.project_name = tk.StringVar(
            value=self.project.name)

        self.dev_base_dir = tk.StringVar(
            value=self.project.dev_base_dir)
        self.development_directory_tooltip_text = tk.StringVar(
            value=dev_dir_tooltip)

        self.dev_source_dir = tk.StringVar(
            value=self.project.dev_source_dir)
        self.source_directory_tooltip_text = tk.StringVar(
            value=source_dir_tooltip)

        self.dev_image_dir = tk.StringVar(
            value=self.project.dev_image_dir)
        self.image_directory_tooltip_text = tk.StringVar(
            value=image_dir_tooltip)

        self.win_source_dir = tk.StringVar(
            value=self.project.win_source_dir)
        self.company_name = tk.StringVar(value=self.project.company_name)
        self.win_install_path = tk.StringVar(
            value=self.project.win_install_path)
        self.start_menu_text = tk.StringVar(value=self.project.start_menu_text)
        self.version = tk.StringVar(value=self.project.version)
        self.update_requirements = tk.BooleanVar(value=False)
        self.close_on_build = tk.BooleanVar(value=True)

        self.project_id.trace_add('write', self._project_name_changed)
        self.company_name.trace_add('write', self._company_name_changed)
        self.email.trace_add('write', self._company_name_changed)

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
        frame = ttk.Frame(master)
        frame.columnconfigure(0, weight=1)

        row = 0
        # Project name
        project_frame = self._project_frame(frame)
        project_frame.grid(row=row, column=0, sticky=tk.EW)

        row += 1
        # Development dirs
        separator = separator_frame(frame, 'Development directories')
        separator.grid(row=row, column=0, sticky=tk.EW, padx=PAD)

        row += 1
        # Project dir
        local_frame = self._local_frame(frame)
        local_frame.grid(row=row, column=0, sticky=tk.EW)

        row += 1
        separator = separator_frame(frame, 'Windows')
        separator.grid(row=row, column=0, sticky=tk.EW, padx=PAD)

        row += 1
        windows_frame = self._windows_frame(frame)
        windows_frame.grid(row=row, column=0, sticky=tk.EW)

        row += 1
        separator = separator_frame(frame, 'Build')
        separator.grid(row=row, column=0, sticky=tk.EW, padx=PAD)

        row += 1
        # Close after build
        check_button = tk.Checkbutton(frame, text='Update requirements.txt',
                                      variable=self.update_requirements)
        check_button.grid(row=row, column=0, sticky=tk.W)

        row += 1
        # Close after build
        check_button = tk.Checkbutton(frame, text='Close after build',
                                      variable=self.close_on_build)
        check_button.grid(row=row, column=0, sticky=tk.W)

        return frame

    def _project_frame(self, master: tk.Frame) -> ttk.Frame:
        # pylint: disable=no-member)
        frame = ttk.Frame(master)
        frame.columnconfigure(1, weight=1)

        row = 0
        # Project name
        label = ttk.Label(frame, text='Project id')
        label.grid(row=0, column=0, sticky=tk.E, padx=PAD, pady=PAD)
        entry = ttk.Entry(frame, textvariable=self.project_id)
        entry.grid(row=0, column=1, sticky=tk.EW, pady=PAD)
        if self.mode == MODES['new']:
            entry.focus_set()
        else:
            entry.configure(state='disable')

        row += 1
        # Windows project dir
        label = ttk.Label(frame, text='Project name')
        label.grid(row=row, column=0, sticky=tk.E, padx=PAD, pady=PAD)
        entry = ttk.Entry(frame, textvariable=self.project_name)
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
        # Author
        label = ttk.Label(frame, text='Email')
        label.grid(row=row, column=0, sticky=tk.E, padx=PAD, pady=PAD)
        entry = ttk.Entry(frame, textvariable=self.email)
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

        return frame

    def _local_frame(self, master: tk.Frame) -> ttk.Frame:
        # pylint: disable=no-member)
        frame = ttk.Frame(master)
        frame.columnconfigure(1, weight=1)

        row = 0
        label = ttk.Label(frame, text='Project directory')
        label.grid(row=row, column=0, sticky=tk.E, padx=PAD, pady=PAD)
        entry = ttk.Entry(
            frame, textvariable=self.dev_base_dir)
        entry.grid(row=row, column=1, sticky=tk.EW)
        self._entry_tooltip(entry, self.development_directory_tooltip_text,)
        button = ttk.Button(frame, text=txt.ELLIPSIS,
                            command=self._project_directory)
        button.grid(row=row, column=3, padx=PAD)

        row += 1
        # Source dir
        label = ttk.Label(frame, text='Source directory')
        label.grid(row=row, column=0, sticky=tk.E, padx=PAD, pady=PAD)
        entry = ttk.Entry(frame, textvariable=self.dev_source_dir)
        entry.grid(row=row, column=1, sticky=tk.EW)
        self._entry_tooltip(entry, self.source_directory_tooltip_text,)
        button = ttk.Button(frame, text=txt.ELLIPSIS,
                            command=self._source_directory)
        button.grid(row=row, column=3, padx=PAD)

        row += 1
        # Images dir
        label = ttk.Label(frame, text='Images directory')
        label.grid(row=row, column=0, sticky=tk.E, padx=PAD, pady=PAD)
        entry = ttk.Entry(frame, textvariable=self.dev_image_dir)
        entry.grid(row=row, column=1, sticky=tk.EW)
        self._entry_tooltip(entry, self.image_directory_tooltip_text,)
        button = ttk.Button(frame, text=txt.ELLIPSIS,
                            command=self._image_directory)
        button.grid(row=row, column=3, padx=PAD)

        return frame

    def _windows_frame(self, master: tk.Frame) -> ttk.Frame:
        # pylint: disable=no-member)
        frame = ttk.Frame(master)
        frame.columnconfigure(1, weight=1)

        row = 0
        # Company name
        label = ttk.Label(frame, text='Company name')
        label.grid(row=row, column=0, sticky=tk.E, padx=PAD, pady=PAD)
        entry = ttk.Entry(frame, textvariable=self.company_name)
        entry.grid(row=row, column=1, sticky=tk.EW)

        row += 1
        # Windows project dir
        label = ttk.Label(frame, text='Windows project directory')
        label.grid(row=row, column=0, sticky=tk.E, padx=PAD, pady=PAD)
        entry = ttk.Entry(frame, textvariable=self.win_source_dir)
        entry.grid(row=row, column=1, sticky=tk.EW)

        row += 1
        # Installation path
        label = ttk.Label(frame, text='Installation path')
        label.grid(row=row, column=0, sticky=tk.E, padx=PAD, pady=PAD)
        entry = ttk.Entry(frame, textvariable=self.win_install_path)
        entry.grid(row=row, column=1, sticky=tk.EW)

        row += 1
        # Start menu text
        label = ttk.Label(frame, text='Start menu text')
        label.grid(row=row, column=0, sticky=tk.E, padx=PAD, pady=PAD)
        entry = ttk.Entry(frame, textvariable=self.start_menu_text)
        entry.grid(row=row, column=1, sticky=tk.EW)

        return frame

    def _button_frame(self, master: tk.Frame) -> tk.Frame:
        frame = ButtonFrame(master, tk.HORIZONTAL)
        frame.buttons = [
            frame.icon_button('save', self._save_project),
            frame.icon_button('build', self._build),
            frame.icon_button('exit', self._dismiss),
        ]
        frame.enable(False)
        return frame

    def _entry_tooltip(self, entry: ttk.Entry, tk_var: tk.StringVar) -> None:
        entry.tooltip = Tooltip(entry, textvariable=tk_var, wrap_length=2000)
        entry.bind('<Enter>', entry.tooltip.onEnter)
        entry.bind('<Leave>', entry.tooltip.onLeave)

    def _project_directory(self, *args) -> None:
        # pylint: disable=no-member)
        initialdir = self.dev_base_dir.get()
        if not initialdir:
            initialdir = self.config.projects_directory
        dlg = filedialog.askdirectory(
            initialdir=initialdir,
        )
        if dlg:
            self.dev_base_dir.set(dlg)

    def _source_directory(self, *args) -> None:
        dlg = filedialog.askdirectory(
            initialdir=self.dev_base_dir.get(),
        )
        if dlg:
            self.dev_source_dir.set(dlg)

    def _image_directory(self, *args) -> None:
        dlg = filedialog.askdirectory(
            initialdir=self.dev_base_dir.get(),
        )
        if dlg:
            self.dev_image_dir.set(dlg)
            self._source_directory_changed()

    def _source_directory_changed(self) -> None:
        if not self.dev_source_dir.get():
            return
        try:
            src_dir = Path(self.dev_source_dir.get(), '_version.py')
            with open(src_dir, 'r', encoding='utf-8') as f_version:
                version = f_version.read()

                version_re = r'[0-9]{1,}.[0-9]{1,}.[0-9]{1,}'
                match = re.search(version_re, version)
                if not match:
                    print('*** Invalid _version.py file structure ***')
                    return
                self.version.set(match.group())

        except FileNotFoundError:
            logger.error('No _version file found')

    def _project_name_changed(self, *args) -> None:
        # pylint: disable=no-member)
        if self.mode != MODES['new']:
            return

        name = self.project_name.get()
        self.description.set(self._name_upper(name))
        self.project_name.set(name)
        self.exe_name.set(self._name_upper(name, delimiter=''))
        self.start_menu_text.set(self.description.get())
        self.win_install_path.set(
            f'{self.config.windows_project_directory}\\{name}'
        )
        self.win_source_dir.set(
            f'{self.config.windows_project_directory}\\{name}'
        )
        self.win_install_path.set(
            f'{self.company_name.get()}\\{self.exe_name.get()}'
        )

    def _company_name_changed(self, *args) -> None:
        if self.company_name.get():
            self.win_install_path.set(
                f'\\{self.company_name.get()}\\{self.exe_name.get()}'
            )
        else:
            self.win_install_path.set(
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
        self._update_project()
        self.project_server.projects[self.project.name] = self.project
        self.project_server.save_projects()

    def _check_spaces_in_name(self) -> bool:
        if ' ' not in self.project_id.get():
            return True

        dlg = messagebox.askyesno(
            '',
            'There are spaces in the project name. Is this correct?',
            parent=self.root,
        )
        return bool(dlg)

    def _build(self, *args) -> None:
        if not self._check_spaces_in_name():
            return

        config = read_config()
        self._update_project()
        result = self.project.build(config, self.update_requirements.get())
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

        # Project name (e.g. directors_rota)
        self.project.name = self.project_name.get()

        self.project.description = self.description.get()
        self.project.author = self.author.get()
        self.project.email = self.email.get()
        self.project.version = self.version.get()

        # Project directory
        self.project.dev_base_dir = self.dev_base_dir.get()

        # Source directory
        self.project.dev_source_dir = self.dev_source_dir.get()

        # Image directory
        self.project.dev_image_dir = self.dev_image_dir.get()

        # Windows project directory
        self.project.win_source_dir = self.win_source_dir.get()

        # Installation path
        self.project.win_install_path = self.win_install_path.get()

        self.project.exe_name = self.exe_name.get()
        self.project.company_name = self.company_name.get()
        self.project.start_menu_text = self.start_menu_text.get()

    def _dismiss(self, *args) -> None:
        self.root.destroy()
