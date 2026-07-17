# settings.py
from __future__ import annotations

import json
import os
from pathlib import Path


class Settings:
    """Loads and persists user-configurable timer and message settings."""

    DEFAULT_REMINDER_MINUTES = 10
    DEFAULT_SNOOZE_MINUTES = 5
    DEFAULT_CUSTOM_MESSAGE = ""

    def __init__(self) -> None:
        config_dir = Path(os.getenv("APPDATA", str(Path.home()))) / "WaterBuddy"
        config_dir.mkdir(parents=True, exist_ok=True)
        self.path = config_dir / "config.json"

        self.custom_assets_dir = config_dir / "custom_assets"
        self.custom_assets_dir.mkdir(parents=True, exist_ok=True)

        self.reminder_minutes = self.DEFAULT_REMINDER_MINUTES
        self.snooze_minutes = self.DEFAULT_SNOOZE_MINUTES
        self.custom_message = self.DEFAULT_CUSTOM_MESSAGE
        self._load()

    def _load(self) -> None:
        if not self.path.exists():
            return

        try:
            data = json.loads(self.path.read_text())
        except (json.JSONDecodeError, OSError):
            return

        self.reminder_minutes = int(data.get("reminder_minutes", self.reminder_minutes))
        self.snooze_minutes = int(data.get("snooze_minutes", self.snooze_minutes))
        self.custom_message = str(data.get("custom_message", self.custom_message))

    def save(self, reminder_minutes: int, snooze_minutes: int, custom_message: str) -> None:
        self.reminder_minutes = reminder_minutes
        self.snooze_minutes = snooze_minutes
        self.custom_message = custom_message

        data = {
            "reminder_minutes": self.reminder_minutes,
            "snooze_minutes": self.snooze_minutes,
            "custom_message": self.custom_message,
        }
        self.path.write_text(json.dumps(data, indent=2))
