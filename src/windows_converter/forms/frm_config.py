"""ConfigFrame for Windows converter."""

import tkinter as tk
from tkinter import ttk, filedialog
from pathlib import Path

from psiutils.buttons import ButtonFrame, Button
from psiutils.constants import PAD
from psiutils.utilities import window_resize

from config import read_config, save_config
from constants import APP_TITLE
import text

FRAME_TITLE = f'{APP_TITLE} - {text.CONFIG}'


class ConfigFrame():
    def __init__(self, parent: tk.Frame) -> None:
        self.root = tk.Toplevel(parent.root)
        self.parent = parent
        self.config = read_config()

        # tk variables
        self.windows_base_directory = tk.StringVar(
            value=self.config.windows_base_directory)
        self.windows_project_directory = tk.StringVar(
            value=self.config.windows_project_directory)
        self.author = tk.StringVar(value=self.config.author)

        self.windows_base_directory.trace_add(
            'write', self._check_value_changed)
        self.windows_project_directory.trace_add(
            'write', self._check_value_changed)
        self.author.trace_add('write', self._check_value_changed)

        self.show()

    def show(self) -> None:
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
        frame = ttk.Frame(master)
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)

        label = ttk.Label(frame, text='Windows base directory')
        label.grid(row=0, column=0, sticky=tk.E, padx=PAD, pady=PAD)
        entry = ttk.Entry(frame, textvariable=self.windows_base_directory)
        entry.grid(row=0, column=1, sticky=tk.EW)
        button = ttk.Button(frame, text=text.ELLIPSIS,
                            command=self._get_windows_base_directory)
        button.grid(row=0, column=2, padx=PAD)

        label = ttk.Label(frame, text='Author')
        label.grid(row=1, column=0, sticky=tk.E, padx=PAD, pady=PAD)
        entry = ttk.Entry(frame, textvariable=self.author)
        entry.grid(row=1, column=1, sticky=tk.EW)

        label = ttk.Label(frame, text='Windows project directory')
        label.grid(row=2, column=0, sticky=tk.E, padx=PAD, pady=PAD)
        entry = ttk.Entry(frame, textvariable=self.windows_project_directory)
        entry.grid(row=2, column=1, sticky=tk.EW)

        return frame

    def _button_frame(self, master: tk.Frame) -> tk.Frame:
        frame = ButtonFrame(master, tk.HORIZONTAL)
        frame.buttons = [
            Button(
                frame,
                text=text.SAVE,
                command=self._save_config,
                underline=0,
                dimmable=True),
            Button(
                frame,
                text=text.EXIT,
                command=self._dismiss,
                sticky=tk.E,
                underline=1),
        ]
        frame.enable(False)
        return frame

    def _get_windows_base_directory(self, *args):
        dlg = filedialog.askdirectory(
            initialdir=self.windows_base_directory.get(),
        )
        if dlg:
            self.windows_base_directory.set(dlg)

    def _value_changed(self) -> bool:
        windows_base_directory = self.config.windows_base_directory
        windows_project_directory = self.config.windows_project_directory
        return (
            self.windows_base_directory.get() != windows_base_directory or
            self.windows_project_directory.get() != windows_project_directory or  # noqa: E501
            self.author.get() != self.config.author or
            ...
        )

    def _check_value_changed(self, *args) -> None:
        enable = False
        if self._value_changed():
            enable = True
        self.button_frame.enable(enable)

    def _save_config(self, *args) -> None:
        self.config.update(
            'windows_base_directory', self.windows_base_directory.get())
        self.config.update(
            'windows_project_directory', self.windows_project_directory.get())
        self.config.update('author', self.author.get())
        save_config(self.config)
        self._dismiss()

    def _dismiss(self, *args) -> None:
        self.root.destroy()
