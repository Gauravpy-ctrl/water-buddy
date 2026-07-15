# reminder.py
from __future__ import annotations

import tkinter as tk
from typing import Callable


class ReminderManager:
    """Manages reminder and snooze timers through tkinter's event loop."""

    def __init__(
        self,
        root: tk.Tk,
        on_reminder: Callable[[], None],
        reminder_minutes: int,
        snooze_minutes: int,
    ) -> None:
        self.root = root
        self.on_reminder = on_reminder
        self.reminder_minutes = reminder_minutes
        self.snooze_minutes = snooze_minutes
        self._timer_id: str | None = None
        self._active_kind: str | None = None

    def start_initial_timer(self) -> None:
        """Start the normal reminder timer."""
        self.cancel()
        self._active_kind = "reminder"
        self._timer_id = self.root.after(
            self.reminder_minutes * 60 * 1000,
            self._trigger,
        )

    def start_snooze_timer(self) -> None:
        """Start the snooze timer."""
        self.cancel()
        self._active_kind = "snooze"
        self._timer_id = self.root.after(
            self.snooze_minutes * 60 * 1000,
            self._trigger,
        )

    def apply_new_intervals(self, reminder_minutes: int, snooze_minutes: int) -> None:
        """Update both intervals. If a timer is currently running, restart
        it immediately so the change takes effect right away instead of
        waiting for the next cycle."""
        self.reminder_minutes = reminder_minutes
        self.snooze_minutes = snooze_minutes

        if self._active_kind == "reminder":
            self.start_initial_timer()
        elif self._active_kind == "snooze":
            self.start_snooze_timer()

    def cancel(self) -> None:
        """Cancel any currently active timer."""
        if self._timer_id is not None:
            self.root.after_cancel(self._timer_id)
            self._timer_id = None
        self._active_kind = None

    def _trigger(self) -> None:
        """Execute the reminder callback."""
        self._timer_id = None
        self._active_kind = None
        self.on_reminder()
