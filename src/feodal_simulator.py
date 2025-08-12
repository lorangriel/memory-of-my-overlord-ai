"""Simplified fragment of the feodal simulator GUI.

This module demonstrates a safe pattern for updating Tkinter widgets
that may have been destroyed. Without this guard Tkinter raises a
``TclError`` when a callback tries to access a widget after its
destruction.
"""

from __future__ import annotations

import tkinter as tk


class JarldomEditor:
    """Editor managing work display for a jarldom."""

    def __init__(self, master: tk.Misc | None = None) -> None:
        self.master = master or tk.Tk()
        self.work_need_entry = tk.Entry(self.master)
        self.work_need_entry.pack()

    def _update_jarldom_work_display(self) -> None:
        """Safely update the work need entry if it still exists."""

        if getattr(self, "work_need_entry", None) and self.work_need_entry.winfo_exists():
            self.work_need_entry.config(foreground="black")

    def update_day_laborers(self) -> None:
        """Callback updating laborer display, guarded against missing widget."""

        if not (getattr(self, "work_need_entry", None) and self.work_need_entry.winfo_exists()):
            return
        self._update_jarldom_work_display()
