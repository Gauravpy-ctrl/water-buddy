# animations.py
from __future__ import annotations

from pathlib import Path
from typing import Sequence

import tkinter as tk
from PIL import Image, ImageTk


class AnimationManager:
    """Loads and displays pet animation frames."""

    FRAME_DELAY_MS = 120

    def __init__(self, root: tk.Tk, image_label: tk.Label, assets_dir: Path) -> None:
        self.root = root
        self.image_label = image_label
        self.assets_dir = assets_dir

        self._after_id: str | None = None
        self._current_frames: list[ImageTk.PhotoImage] = []
        self._frame_index = 0

        self.idle = self._load_image("idle.png")
        self.happy = self._load_image("happy.png")
        self.angry = self._load_image("angry.png")

        self.walk_in_frames = self._load_frames(
            ["walk_in1.png", "walk_in2.png", "walk_in3.png", "walk_in4.png"]
        )
        self.walk_out_frames = self._load_frames(
            ["walk_out1.png", "walk_out2.png", "walk_out3.png", "walk_out4.png"]
        )

    def _load_image(self, filename: str) -> ImageTk.PhotoImage:
        path = self.assets_dir / filename
        if not path.exists():
            raise FileNotFoundError(f"Missing asset: {path}")

        image = Image.open(path).convert("RGBA")

        # Keep all frames the same size. NEAREST avoids interpolating the
        # alpha channel at sprite edges -- bicubic/bilinear blending would
        # produce semi-transparent edge pixels that pick up the window's
        # -transparentcolor key as a visible colored fringe when composited.
        image = image.resize((220, 220), Image.NEAREST)

        return ImageTk.PhotoImage(image)

    def _load_frames(self, filenames: Sequence[str]) -> list[ImageTk.PhotoImage]:
        return [self._load_image(filename) for filename in filenames]

    def _set_image(self, image: ImageTk.PhotoImage) -> None:
        self.image_label.configure(image=image)
        self.image_label.image = image

    def _play_loop(self) -> None:
        if not self._current_frames:
            return

        self._set_image(self._current_frames[self._frame_index])
        self._frame_index = (self._frame_index + 1) % len(self._current_frames)
        self._after_id = self.root.after(self.FRAME_DELAY_MS, self._play_loop)

    def _start_loop(self, frames: list[ImageTk.PhotoImage]) -> None:
        self.stop()
        self._current_frames = frames
        self._frame_index = 0
        self._play_loop()

    def play_walk_in(self) -> None:
        self._start_loop(self.walk_in_frames)

    def play_walk_out(self) -> None:
        self._start_loop(self.walk_out_frames)

    def set_idle(self) -> None:
        self.stop()
        self._set_image(self.idle)

    def set_happy(self) -> None:
        self.stop()
        self._set_image(self.happy)

    def set_angry(self) -> None:
        self.stop()
        self._set_image(self.angry)

    def stop(self) -> None:
        if self._after_id is not None:
            self.root.after_cancel(self._after_id)
            self._after_id = None