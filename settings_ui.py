# settings_ui.py
from __future__ import annotations

import tkinter as tk
from tkinter import messagebox
from typing import Callable


class SettingsDialog:
    """A small modal dialog for customizing the reminder/snooze intervals
    and the reminder message."""

    def __init__(
        self,
        parent: tk.Tk,
        current_reminder_minutes: int,
        current_snooze_minutes: int,
        current_custom_message: str,
        on_save: Callable[[int, int, str], None],
    ) -> None:
        self.on_save = on_save

        self.window = tk.Toplevel(parent)
        self.window.title("Water Buddy Settings")
        self.window.resizable(False, False)
        self.window.attributes("-topmost", True)

        frame = tk.Frame(self.window, padx=20, pady=16)
        frame.pack()

        tk.Label(frame, text="Remind me every").grid(row=0, column=0, sticky="w", pady=6)
        self.reminder_var = tk.StringVar(value=str(current_reminder_minutes))
        tk.Entry(
            frame, textvariable=self.reminder_var, width=6, justify="center"
        ).grid(row=0, column=1, padx=8)
        tk.Label(frame, text="minutes").grid(row=0, column=2, sticky="w")

        tk.Label(frame, text="Snooze for").grid(row=1, column=0, sticky="w", pady=6)
        self.snooze_var = tk.StringVar(value=str(current_snooze_minutes))
        tk.Entry(
            frame, textvariable=self.snooze_var, width=6, justify="center"
        ).grid(row=1, column=1, padx=8)
        tk.Label(frame, text="minutes").grid(row=1, column=2, sticky="w")

        tk.Label(frame, text="Custom message").grid(row=2, column=0, sticky="w", pady=(12, 2))
        self.message_var = tk.StringVar(value=current_custom_message)
        tk.Entry(
            frame, textvariable=self.message_var, width=34
        ).grid(row=3, column=0, columnspan=3, sticky="we", pady=(0, 4))
        tk.Label(
            frame,
            text="Leave blank to use the default greeting.",
            font=("Segoe UI", 8),
            fg="#666666",
        ).grid(row=4, column=0, columnspan=3, sticky="w")

        button_row = tk.Frame(frame)
        button_row.grid(row=5, column=0, columnspan=3, pady=(14, 0))
        tk.Button(
            button_row, text="Save", width=10, command=self._handle_save
        ).pack(side="left", padx=5)
        tk.Button(
            button_row, text="Cancel", width=10, command=self.window.destroy
        ).pack(side="left", padx=5)

        self.window.update_idletasks()
        self._center_on_screen()

        self.window.lift()
        self.window.focus_force()

    def _center_on_screen(self) -> None:
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.window.geometry(f"+{x}+{y}")

    def _handle_save(self) -> None:
        try:
            reminder_minutes = int(self.reminder_var.get())
            snooze_minutes = int(self.snooze_var.get())
        except ValueError:
            messagebox.showerror(
                "Invalid input",
                "Please enter whole numbers for both fields.",
                parent=self.window,
            )
            return

        if reminder_minutes < 1 or snooze_minutes < 1:
            messagebox.showerror(
                "Invalid input",
                "Minutes must be at least 1.",
                parent=self.window,
            )
            return

        custom_message = self.message_var.get().strip()

        self.on_save(reminder_minutes, snooze_minutes, custom_message)
        self.window.destroy()
