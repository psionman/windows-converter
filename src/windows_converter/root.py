
"""
 A tkinter application for Windows converter.
"""

import sys
import tkinter as tk

from psiutils.widgets import get_styles
from psiutils.utilities import display_icon

from windows_converter.constants import ICON_FILE
from windows_converter.module_caller import ModuleCaller

from windows_converter.forms.frm_main import MainFrame


class Root():
    def __init__(self) -> None:
        """Create the app's root and loop."""
        root = tk.Tk()
        self.root = root
        display_icon(root, ICON_FILE, ignore_error=True)
        root.protocol("WM_DELETE_WINDOW", root.destroy)

        get_styles()

        dlg = None
        if len(sys.argv) > 1:
            module = sys.argv[1]
            dlg = ModuleCaller(root, module)
        if not dlg or dlg.invalid:
            MainFrame(root)

        root.mainloop()
