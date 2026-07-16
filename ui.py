# ui.py
from __future__ import annotations


import tkinter as tk
from typing import Callable

import customtkinter as ctk


class DesktopPetUI:
    """Builds the transparent always-on-top desktop pet window."""

    TRANSPARENT_COLOR = "#ff00ff"
    BUBBLE_BG = "#fff7df"
    BUBBLE_BORDER = "#3b2f2f"
    TEXT_COLOR = "#2d2525"

    WINDOW_WIDTH = 360
    WINDOW_HEIGHT = 360
    PET_AREA_HEIGHT = 220

    USER_NAME = "Gaurav"

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.on_yes: Callable[[], None] | None = None
        self.on_snooze: Callable[[], None] | None = None

        self._configure_window()
        self._build_layout()

    def _configure_window(self) -> None:
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)

        self.root.wm_attributes(
            "-transparentcolor",
            self.TRANSPARENT_COLOR
        )

        self.root.configure(bg=self.TRANSPARENT_COLOR)
        self.root.withdraw()

    def _build_layout(self) -> None:
        self.container = tk.Frame(
            self.root,
            bg=self.TRANSPARENT_COLOR,
            width=self.WINDOW_WIDTH,
            height=self.WINDOW_HEIGHT,
        )
        self.container.pack(fill="both", expand=True)
        self.container.pack_propagate(False)

        self.bubble_frame = tk.Frame(
            self.container,
            bg=self.BUBBLE_BG,
            highlightbackground=self.BUBBLE_BORDER,
            highlightthickness=3,
            bd=0,
            padx=6,
            pady=6,
        )
        # placed (not packed) so showing/hiding it never triggers a
        # relayout of its sibling image_label -- doing so via pack()
        # left CTkButton's text canvas blank after a pack_forget()/
        # pack() cycle (a Tk geometry-manager redraw quirk, not a
        # customtkinter bug -- reproduced with plain tk.Button too).

        self.message_label = tk.Label(
            self.bubble_frame,
            text="",
            font=("Consolas", 13, "bold"),
            fg=self.TEXT_COLOR,
            bg=self.BUBBLE_BG,
            padx=14,
            pady=10,
            wraplength=320,
            justify="center",
        )
        self.message_label.pack()

        self.button_frame = tk.Frame(self.bubble_frame, bg=self.BUBBLE_BG)
        self.button_frame.pack(pady=(0, 10))

        self.yes_button = ctk.CTkButton(
            self.button_frame,
            text="Yes",
            width=88,
            height=30,
            corner_radius=0,
            fg_color="#6bd17b",
            hover_color="#58bd67",
            text_color="#1d2a1f",
            command=self._handle_yes,
        )
        self.yes_button.grid(row=0, column=0, padx=5)

        self.snooze_button = ctk.CTkButton(
            self.button_frame,
            text="Remind Me In 5 Min",
            width=150,
            height=30,
            corner_radius=0,
            fg_color="#8fd3ff",
            hover_color="#72bdea",
            text_color="#182936",
            command=self._handle_snooze,
        )
        self.snooze_button.grid(row=0, column=1, padx=5)

        self.image_label = tk.Label(
            self.container,
            bg=self.TRANSPARENT_COLOR,
            bd=0,
            highlightthickness=0,
        )
        self.image_label.place(relx=0.5, rely=1.0, y=-8, anchor="s")

        self.hide_bubble()

    def _handle_yes(self) -> None:
        if self.on_yes is not None:
            self.on_yes()

    def _handle_snooze(self) -> None:
        if self.on_snooze is not None:
            self.on_snooze()

    def set_button_handlers(
        self,
        on_yes: Callable[[], None],
        on_snooze: Callable[[], None],
    ) -> None:
        self.on_yes = on_yes
        self.on_snooze = on_snooze

    def show(self) -> None:
        self.root.deiconify()
        self.root.lift()
        self.root.attributes("-topmost", True)

    def hide(self) -> None:
        self.root.withdraw()

    def set_position(self, x: int, y: int) -> None:
        self.root.geometry(f"{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}+{x}+{y}")

    def screen_width(self) -> int:
        return self.root.winfo_screenwidth()

    def screen_height(self) -> int:
        return self.root.winfo_screenheight()

    def window_width(self) -> int:
        return self.WINDOW_WIDTH

    def window_height(self) -> int:
        return self.WINDOW_HEIGHT

    def show_question(self, custom_message: str = "") -> None:
        message = custom_message or f"💧 Hey {self.USER_NAME}! Did you drink water?"
        self.set_message(message)
        self.show_buttons()
        self.show_bubble()

    def show_good_job(self) -> None:
        self.set_message("✨ Good job!")
        self.hide_buttons()
        self.show_bubble()

    def show_come_back(self) -> None:
        self.set_message("😤 Fine... I'll come back.")
        self.hide_buttons()
        self.show_bubble()

    def set_message(self, message: str) -> None:
        self.message_label.configure(text=message)

    def show_buttons(self) -> None:
        self.button_frame.pack(pady=(0, 10))

    def hide_buttons(self) -> None:
        self.button_frame.pack_forget()

    def show_bubble(self) -> None:
        self.bubble_frame.place(relx=0.5, y=8, anchor="n")

    def hide_bubble(self) -> None:
        self.bubble_frame.place_forget()