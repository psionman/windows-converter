"""ConfigFrame for Windows converter."""

import tkinter as tk
from tkinter import ttk, filedialog
from pathlib import Path

from psiutils.buttons import ButtonFrame
from psiutils.constants import PAD
from psiutils.utilities import window_resize

from windows_converter.config import read_config
from windows_converter.constants import APP_TITLE
from windows_converter.text import Text
from windows_converter import logger

txt = Text()
# pylint: disable=no-member)
FRAME_TITLE = f'{APP_TITLE} - {txt.CONFIG}'

FIELDS = {
    'build_base_dir': tk.StringVar,
    'windows_project_directory': tk.StringVar,
    'author': tk.StringVar,
    'email': tk.StringVar,
}


class ConfigFrame():
    def __init__(self, parent: tk.Frame) -> None:
        # pylint: disable=no-member)
        self.root = tk.Toplevel(parent.root)
        self.parent = parent
        config = read_config()
        self.config = config

        for field, f_type in FIELDS.items():
            if f_type is tk.StringVar:
                setattr(self, field, self._stringvar(getattr(config, field)))

        self._show()

    def _stringvar(self, value: str) -> tk.StringVar:
        stringvar = tk.StringVar(value=value)
        stringvar.trace_add('write', self._check_value_changed)
        return stringvar

    def _show(self) -> None:
        # pylint: disable=no-member)
        root = self.root
        root.geometry(self.config.geometry[Path(__file__).stem])
        root.transient(self.parent.root)
        root.title(FRAME_TITLE)
        root.bind('<Configure>',
                  lambda e: window_resize(self, __file__))

        root.rowconfigure(1, weight=1)
        root.columnconfigure(0, weight=1)

        main_frame = self._main_frame(root)
        main_frame.grid(row=0, column=0, sticky=tk.NSEW, padx=PAD, pady=PAD)
        self.button_frame = self._button_frame(root)
        self.button_frame.grid(row=8, column=0, columnspan=9,
                               sticky=tk.EW, padx=PAD, pady=PAD)

        sizegrip = ttk.Sizegrip(root)
        sizegrip.grid(sticky=tk.SE)

    def _main_frame(self, master: tk.Frame) -> ttk.Frame:
        # pylint: disable=no-member)
        frame = ttk.Frame(master)
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)

        row = 0
        label = ttk.Label(frame, text='Windows base directory')
        label.grid(row=row, column=0, sticky=tk.E, padx=PAD, pady=PAD)
        entry = ttk.Entry(frame, textvariable=self.build_base_dir)
        entry.grid(row=row, column=1, sticky=tk.EW)
        button = ttk.Button(frame, text=txt.ELLIPSIS,
                            command=self._get_build_base_dir)
        button.grid(row=row, column=2, padx=PAD)

        row += 1
        label = ttk.Label(frame, text='Author')
        label.grid(row=row, column=0, sticky=tk.E, padx=PAD, pady=PAD)
        entry = ttk.Entry(frame, textvariable=self.author)
        entry.grid(row=row, column=1, sticky=tk.EW)

        row += 1
        label = ttk.Label(frame, text='Email')
        label.grid(row=row, column=0, sticky=tk.E, padx=PAD, pady=PAD)
        entry = ttk.Entry(frame, textvariable=self.email)
        entry.grid(row=row, column=1, sticky=tk.EW)

        row += 1
        label = ttk.Label(frame, text='Windows project directory')
        label.grid(row=row, column=0, sticky=tk.E, padx=PAD, pady=PAD)
        entry = ttk.Entry(frame, textvariable=self.windows_project_directory)
        entry.grid(row=row, column=1, sticky=tk.EW)

        return frame

    def _button_frame(self, master: tk.Frame) -> tk.Frame:
        frame = ButtonFrame(master, tk.HORIZONTAL)
        frame.buttons = [
            frame.icon_button('save', self._save_config, True),
            frame.icon_button('exit', self._dismiss),
        ]
        frame.enable(False)
        return frame

    def _get_build_base_dir(self, *args):
        # pylint: disable=no-member)
        dlg = filedialog.askdirectory(
            initialdir=self.build_base_dir.get(),
        )
        if dlg:
            self.build_base_dir.set(dlg)

    def _check_value_changed(self, *args) -> None:
        enable = bool(self._config_changes())
        self.button_frame.enable(enable)

    def _save_config(self, *args) -> None:
        changes = {field: f'(old value={change[0]}, new_value={change[1]})'
                   for field, change in self._config_changes().items()}

        for field in FIELDS:
            self.config.config[field] = getattr(self, field).get()

        logger.info("Config saved", changes=changes)

        self._dismiss()
        return self.config.save()

    def _config_changes(self) -> dict:
        stored = self.config.config
        return {
            field: (stored[field], getattr(self, field).get())
            for field in FIELDS
            if stored[field] != getattr(self, field).get()
        }

    def _dismiss(self, *args) -> None:
        self.root.destroy()
