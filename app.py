import time

from event import Event, SleepEvent
from state_machine import StateMachine

from flashcard import Flashcard

class App(StateMachine):
    def __init__(self, magtag) -> None:
        super().__init__(self.start)

        self.magtag = magtag
        self.manager = Flashcard()

        self._refresh = False
        self._menu_selection = None

        self._flashcard_button_pressed_switch = self._create_flashcard_button_pressed_switch()
        self._menu_button_pressed_switch = self._create_menu_button_pressed_switch()

        self._start_switch = self._create_start_switch()
        self._flashcard_switch = self._create_flashcard_switch()
        self._menu_switch = self._create_menu_switch()

    def _create_flashcard_button_pressed_switch(self):
        def _pressed_a():
            self.transition_to(self.menu)

        def _pressed_d():
            self.manager.next_word()

            self._refresh = True

        return {
            "A": _pressed_a,
            "D": _pressed_d,
        }

    def _create_menu_button_pressed_switch(self):
        def _pressed_a():
            self.transition_to(self.flashcard)

        def _pressed_b():
            if self._menu_selection == 0:
                self.manager.decrement_mode()
            if self._menu_selection == 1:
                self.manager.decrement_week()

            self._refresh = True

        def _pressed_c():
            if self._menu_selection == 0:
                self.manager.increment_mode()
            if self._menu_selection == 1:
                self.manager.increment_week()

            self._refresh = True

        def _pressed_d():
            self._menu_selection = (self._menu_selection + 1) % 2

            self._refresh = True

        return {
            "A": _pressed_a,
            "B": _pressed_b,
            "C": _pressed_c,
            "D": _pressed_d,
        }

    def _create_start_switch(self):
        def _start():
            # print("App#start: start")
            self.subscribe("update")
            self.subscribe("button_pressed")

            self.transition_to(self.flashcard)

        return {
            "start": _start
        }

    def _create_flashcard_switch(self):
        def _enter(_: Event):
            # print("App#flashcard: enter")
            # Word Label
            self.magtag.add_text(
                "word",
                text_scale=6,
                text_anchor_point=(0.5, 0.5),
                text_position=(
                    self.magtag.display.width // 2,
                    self.magtag.display.height // 2,
                ),
            )
            # Title
            self.magtag.add_text(
                "title",
                text_anchor_point=(0.0, 0.0),
                text_position=(2, 0),
            )
            # Battery Label
            self.magtag.add_text(
                "battery",
                text_anchor_point=(1.0, 0.0),
                text_position=(296, 0),
            )
            # Button A Label
            self.magtag.add_text(
                "button_a",
                text="Menu",
                text_anchor_point=(0.5, 1.0),
                text_position=(25, 128),
            )
            # Button D Label
            self.magtag.add_text(
                "button_d",
                text="Next Word",
                text_anchor_point=(0.5, 1.0),
                text_position=(245, 128),
            )

            self._refresh = True

        def _exit(_: Event):
            # print("App#flashcard: exit")
            self.magtag.remove_text("word")
            self.magtag.remove_text("battery")
            self.magtag.remove_text("button_a")
            self.magtag.remove_text("button_d")

        def _update(_: Event):
            # print("App#flashcard: update")
            title = "{}:{}:{}".format(
                self.manager.mode_text,
                self.manager.week_text,
                self.manager._word + 1,
            )
            print("{} {}".format(title, self.manager.word_text))
            self.magtag.set_text("title", title)
            self.magtag.set_text("word", self.manager.word_text)
            self.magtag.set_text(
                "battery",
                "{:.2f}V".format(self.magtag.battery),
            )

            self.publish(SleepEvent)

        def _button_pressed(event: Event):
            # print("App#flashcard: button_pressed {}".format(event.button))
            self._flashcard_button_pressed_switch.get(event.button, lambda: None)()

        return {
            "enter": _enter,
            "exit": _exit,
            "update": self.update(_update),
            "button_pressed": _button_pressed,
        }

    def _create_menu_switch(self):
        def _enter(_: Event):
            # print("App#menu: enter")
            # Menu Label
            self.magtag.add_text(
                "menu",
                text_scale=2,
                text_anchor_point=(0.5, 0.5),
                text_position=(
                    self.magtag.display.width // 2,
                    self.magtag.display.height // 2,
                ),
            )
            # Button A Label
            self.magtag.add_text(
                "button_a",
                text="Exit",
                text_anchor_point=(0.5, 1.0),
                text_position=(25, 128),
            )

            self._refresh = True
            self._menu_selection = 0

        def _exit(_: Event):
            # print("App#menu: exit")
            self.magtag.remove_text("menu")
            self.magtag.remove_text("button_a")

            # self.manager.shuffle_words()

        def _update(_: Event):
            # print("App#menu: update")
            mode = "[{}]".format(self.manager.mode_text) if self._menu_selection == 0 else self.manager.mode_text
            week = "[{}]".format(self.manager.week_text) if self._menu_selection == 1 else self.manager.week_text

            self.magtag.set_text("menu", "{}:{}".format(mode, week))

        def _button_pressed(event: Event):
            # print("App#menu: button_pressed {}".format(event.button))
            self._menu_button_pressed_switch.get(event.button, lambda: None)()

        return {
            "enter": _enter,
            "exit": _exit,
            "update": self.update(_update),
            "button_pressed": _button_pressed,
        }

    def update(self, update):
        def refresh(*args):
            if self._refresh:
                update(*args)

                while True:
                    try:
                        self.magtag.display.refresh()

                        self._refresh = False

                        return
                    except RuntimeError:
                        time.sleep(1)
        return refresh

    def start(self, event: Event) -> None:
        self._start_switch.get(event.name, lambda: None)()

    def flashcard(self, event: Event) -> None:
        self._flashcard_switch.get(event.name, lambda _: None)(event)

    def menu(self, event: Event) -> None:
        self._menu_switch.get(event.name, lambda _: None)(event)
