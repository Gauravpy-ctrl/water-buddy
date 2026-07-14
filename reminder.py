# reminder.py
from __future__ import annotations

import tkinter as tk
from typing import Callable


class ReminderManager:
    """Manages reminder and snooze timers through tkinter's event loop."""

    REMINDER_INTERVAL_MS = 10 * 60 * 1000
    SNOOZE_INTERVAL_MS = 5 * 60 * 1000

    def __init__(self, root: tk.Tk, on_reminder: Callable[[], None]) -> None:
        self.root = root
        self.on_reminder = on_reminder
        self._timer_id: str | None = None

    def start_initial_timer(self) -> None:
        """Start the normal 10-minute reminder timer."""
        self.cancel()

        self._timer_id = self.root.after(
            self.REMINDER_INTERVAL_MS,
            self._trigger,
        )

    def start_snooze_timer(self) -> None:
        """Start the 5-minute snooze timer."""
        self.cancel()

        self._timer_id = self.root.after(
            self.SNOOZE_INTERVAL_MS,
            self._trigger,
        )

    def cancel(self) -> None:
        """Cancel any currently active timer."""
        if self._timer_id is not None:
            self.root.after_cancel(self._timer_id)
            self._timer_id = None

    def _trigger(self) -> None:
        """Execute the reminder callback."""
        self._timer_id = None
        self.on_reminder()