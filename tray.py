# tray.py
from __future__ import annotations

import threading
from pathlib import Path
from typing import Callable

import pystray
from PIL import Image


class TrayIcon:
    """Background system tray icon with a right-click menu. Runs its own
    message loop on a daemon thread so it doesn't block tkinter's mainloop;
    callbacks fire on that thread, so callers must marshal any tkinter work
    back onto the main thread (e.g. via root.after(0, ...))."""

    def __init__(
        self,
        icon_path: Path,
        on_open_settings: Callable[[], None],
        on_customize_images: Callable[[], None],
        on_quit: Callable[[], None],
    ) -> None:
        image = Image.open(icon_path)
        menu = pystray.Menu(
            pystray.MenuItem("Set Reminder Timer...", lambda icon, item: on_open_settings()),
            pystray.MenuItem("Customize Pet Images...", lambda icon, item: on_customize_images()),
            pystray.MenuItem("Quit", lambda icon, item: on_quit()),
        )
        self.icon = pystray.Icon("water_buddy", image, "Water Buddy", menu)

    def start(self) -> None:
        threading.Thread(target=self.icon.run, daemon=True).start()

    def stop(self) -> None:
        self.icon.stop()
