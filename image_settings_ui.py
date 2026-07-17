# image_settings_ui.py
from __future__ import annotations

import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox
from typing import Callable

from image_customizer import prepare_custom_image

POSES = [
    ("Idle", "idle", ["idle.png"]),
    ("Happy", "happy", ["happy.png"]),
    ("Angry", "angry", ["angry.png"]),
    ("Walk-in (4 frames)", "walk_in", [
        "walk_in1.png", "walk_in2.png", "walk_in3.png", "walk_in4.png",
    ]),
    ("Walk-out (4 frames)", "walk_out", [
        "walk_out1.png", "walk_out2.png", "walk_out3.png", "walk_out4.png",
    ]),
]

IMAGE_FILETYPES = [("Images", "*.png *.jpg *.jpeg *.bmp *.gif")]


class ImagePickerDialog:
    """Lets the user replace the pet's sprites with their own images,
    pose by pose. Frames for walk-in/walk-out are picked via a single
    multi-select dialog, used in selection order."""

    def __init__(
        self,
        parent: tk.Tk,
        custom_assets_dir: Path,
        on_change: Callable[[], None],
    ) -> None:
        self.custom_assets_dir = custom_assets_dir
        self.custom_assets_dir.mkdir(parents=True, exist_ok=True)
        self.on_change = on_change
        self.status_vars: dict[str, tuple[tk.StringVar, list[str]]] = {}

        self.window = tk.Toplevel(parent)
        self.window.title("Customize Pet Images")
        self.window.resizable(False, False)
        self.window.attributes("-topmost", True)

        frame = tk.Frame(self.window, padx=20, pady=16)
        frame.pack()

        tk.Label(
            frame,
            text=(
                "For best results, use PNGs with a transparent background.\n"
                "For the 4-frame walk animations, ctrl+click all 4 files in "
                "walking order."
            ),
            font=("Segoe UI", 8),
            fg="#666666",
            wraplength=340,
            justify="left",
        ).grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 10))

        row = 1
        for label, key, filenames in POSES:
            tk.Label(frame, text=label, width=18, anchor="w").grid(
                row=row, column=0, sticky="w", pady=4
            )

            status_var = tk.StringVar()
            self.status_vars[key] = (status_var, filenames)
            tk.Label(frame, textvariable=status_var, width=8, fg="#3b7d3b").grid(
                row=row, column=1
            )

            tk.Button(
                frame,
                text="Choose...",
                width=10,
                command=lambda k=key, f=filenames: self._choose(k, f),
            ).grid(row=row, column=2, padx=4)
            row += 1

        self._refresh_status()

        button_row = tk.Frame(frame)
        button_row.grid(row=row, column=0, columnspan=3, pady=(14, 0))
        tk.Button(
            button_row, text="Reset All to Default", command=self._reset_all
        ).pack(side="left", padx=5)
        tk.Button(
            button_row, text="Close", width=10, command=self.window.destroy
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

    def _refresh_status(self) -> None:
        for status_var, filenames in self.status_vars.values():
            all_custom = all(
                (self.custom_assets_dir / name).exists() for name in filenames
            )
            status_var.set("Custom" if all_custom else "Default")

    def _choose(self, key: str, filenames: list[str]) -> None:
        count = len(filenames)
        paths = filedialog.askopenfilenames(
            title=f"Choose {count} image(s) for {key}",
            filetypes=IMAGE_FILETYPES,
            parent=self.window,
        )

        if not paths:
            return

        if len(paths) != count:
            messagebox.showerror(
                "Wrong number of files",
                f"Please select exactly {count} image(s) "
                f"(you selected {len(paths)}).",
                parent=self.window,
            )
            return

        try:
            for source, dest_name in zip(paths, filenames):
                prepare_custom_image(Path(source), self.custom_assets_dir / dest_name)
        except Exception as exc:
            messagebox.showerror(
                "Couldn't process image",
                f"Something went wrong reading that image:\n{exc}",
                parent=self.window,
            )
            return

        self._refresh_status()
        self.on_change()

    def _reset_all(self) -> None:
        if not messagebox.askyesno(
            "Reset to default",
            "Remove all custom images and use the default pet again?",
            parent=self.window,
        ):
            return

        for _, filenames in self.status_vars.values():
            for filename in filenames:
                path = self.custom_assets_dir / filename
                if path.exists():
                    path.unlink()

        self._refresh_status()
        self.on_change()
