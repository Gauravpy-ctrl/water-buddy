# main.py
 
from __future__ import annotations


from enum import Enum, auto
from pathlib import Path
import tkinter as tk

import customtkinter as ctk

from animations import AnimationManager
from reminder import ReminderManager
from ui import DesktopPetUI


class PetState(Enum):
    HIDDEN = auto()
    WALKING_IN = auto()
    IDLE = auto()
    ASKING = auto()
    HAPPY = auto()
    ANGRY = auto()
    WALKING_OUT = auto()


class AppController:
    """Connects UI, animation, timers, and pet state transitions."""

    MOVE_DELAY_MS = 16
    MOVE_STEP_PX = 5
    TARGET_MARGIN_RIGHT = 90
    TARGET_MARGIN_BOTTOM = 70
    RESPONSE_DELAY_MS = 1500

    def __init__(self) -> None:
        ctk.set_appearance_mode("light")

        self.root = tk.Tk()
        self.root.title("Water Buddy")

        self.ui = DesktopPetUI(self.root)
        self.animations = AnimationManager(
            root=self.root,
            image_label=self.ui.image_label,
            assets_dir=Path(__file__).resolve().parent / "assets",
        )
        self.reminders = ReminderManager(self.root, self.handle_reminder)

        self.state = PetState.HIDDEN
        self.x = 0
        self.y = 0
        self.target_x = 0
        self.move_after_id: str | None = None

        self.ui.set_button_handlers(
            on_yes=self.handle_yes_clicked,
            on_snooze=self.handle_snooze_clicked,
        )

    def run(self) -> None:
        self.enter_hidden()
        self.reminders.start_initial_timer()
        self.root.mainloop()

    def transition_to(self, state: PetState) -> None:
        self.state = state

    def enter_hidden(self) -> None:
        self.transition_to(PetState.HIDDEN)
        self._cancel_movement()
        self.animations.stop()
        self.ui.hide_bubble()
        self.ui.hide()

    def handle_reminder(self) -> None:
        if self.state is not PetState.HIDDEN:
            return
        self.start_walk_in()

    def start_walk_in(self) -> None:
        self.transition_to(PetState.WALKING_IN)

        screen_w = self.ui.screen_width()
        screen_h = self.ui.screen_height()

        self.x = screen_w + 20
        self.y = screen_h - self.ui.window_height() - self.TARGET_MARGIN_BOTTOM
        self.target_x = screen_w - self.ui.window_width() - self.TARGET_MARGIN_RIGHT

        self.ui.hide_bubble()
        self.ui.set_position(self.x, self.y)
        self.ui.show()

        self.animations.play_walk_in()
        self._walk_in_step()

    def _walk_in_step(self) -> None:
        if self.state is not PetState.WALKING_IN:
            return

        self.x -= self.MOVE_STEP_PX

        if self.x <= self.target_x:
            self.x = self.target_x
            self.ui.set_position(self.x, self.y)
            self.enter_asking()
            return

        self.ui.set_position(self.x, self.y)
        self.move_after_id = self.root.after(
            self.MOVE_DELAY_MS,
            self._walk_in_step
        )

    def enter_asking(self) -> None:
        self.transition_to(PetState.IDLE)
        self.animations.set_idle()

        self.transition_to(PetState.ASKING)
        self.ui.show_question()

    def handle_yes_clicked(self) -> None:
        if self.state is not PetState.ASKING:
            return

        self.transition_to(PetState.HAPPY)
        self.animations.set_happy()
        self.ui.show_good_job()

        # Start next 10-minute reminder
        self.reminders.start_initial_timer()

        self.root.after(
            self.RESPONSE_DELAY_MS,
            self.start_walk_out
        )

    def handle_snooze_clicked(self) -> None:
        if self.state is not PetState.ASKING:
            return

        self.transition_to(PetState.ANGRY)
        self.animations.set_angry()
        self.ui.show_come_back()

        self.reminders.start_snooze_timer()

        self.root.after(
            self.RESPONSE_DELAY_MS,
            self.start_walk_out
        )

    def start_walk_out(self) -> None:
        if self.state not in {
            PetState.HAPPY,
            PetState.ANGRY,
            PetState.ASKING,
        }:
            return

        self.transition_to(PetState.WALKING_OUT)

        self.ui.hide_bubble()
        self.animations.play_walk_out()

        self._walk_out_step()

    def _walk_out_step(self) -> None:
        if self.state is not PetState.WALKING_OUT:
            return

        self.x += self.MOVE_STEP_PX
        self.ui.set_position(self.x, self.y)

        if self.x >= self.ui.screen_width() + 20:
            self.enter_hidden()
            return

        self.move_after_id = self.root.after(
            self.MOVE_DELAY_MS,
            self._walk_out_step
        )

    def _cancel_movement(self) -> None:
        if self.move_after_id is not None:
            self.root.after_cancel(self.move_after_id)
            self.move_after_id = None


if __name__ == "__main__":
    AppController().run()