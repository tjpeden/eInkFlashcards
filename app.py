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

    def update(self, update):
        def refresh():
            if self._refresh:
                update()

                while True:
                    try:
                        self.magtag.display.refresh()

                        self._refresh = False

                        return
                    except RuntimeError:
                        time.sleep(1)
        return refresh

    def start(self, event: Event) -> None:
        def _start():
            self.subscribe("update")
            self.subscribe("button_pressed")

            self.transition_to(self.flashcard)

        switch = {
            "start": _start
        }

        if event.name in switch:
            switch[event.name]()

    def flashcard(self, event: Event) -> None:
        def _enter():
            print("flashcard: enter")
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
            # Battery Label
            self.magtag.add_text(
                "battery",
                text_anchor_point=(1.0, 0.0),
                text_position=(296, 0),
            )
            # Button A Label
            self.magtag.add_text(
                "button_a",
                text_anchor_point=(0.5, 1.0),
                text_position=(25, 128),
            )
            # Button D Label
            self.magtag.add_text(
                "button_d",
                text_anchor_point=(0.5, 1.0),
                text_position=(245, 128),
            )

            self.magtag.set_text("button_a", "Menu")
            self.magtag.set_text("button_d", "Next Word")

            self._refresh = True

        def _exit():
            print("flashcard: exit")
            self.magtag.remove_text("word")
            self.magtag.remove_text("battery")
            self.magtag.remove_text("button_a")
            self.magtag.remove_text("button_d")

            self.indices = []

        def _update():
            print("flashcard: update")
            battery = (self.magtag.battery - 3.2) / 1.0 * 100.0

            self.magtag.set_text("word", self.manager.word_text)
            self.magtag.set_text("battery", "{:.0f}%".format(battery))

            self.publish(SleepEvent())

        def _button_pressed():
            print("flashcard: button_pressed")
            def _pressed_a():
                self.transition_to(self.menu)

            def _pressed_d():
                self.manager.next_word()

                self._refresh = True

            button_switch = {
                "A": _pressed_a,
                "D": _pressed_d,
            }

            if event.button in button_switch:
                button_switch[event.button]()

        switch = {
            "enter": _enter,
            "exit": _exit,
            "update": self.update(_update),
            "button_pressed": _button_pressed,
        }

        if event.name in switch:
            switch[event.name]()

    def menu(self, event: Event) -> None:
        def _enter():
            print("menu: enter")

            self._refresh = True
            self._menu_selection = 0

        def _exit():
            print("menu: exit")

        def _update():
            print("menu: update")

        def _button_pressed():
            print("menu: button_pressed {}".format(event.button))
            def _pressed_a():
                pass

            def _pressed_b():
                pass

            def _pressed_c():
                pass

            def _pressed_d():
                pass

            button_switch = {
                "A": _pressed_a,
                "B": _pressed_b,
                "C": _pressed_c,
                "D": _pressed_d,
            }

            if event.button in button_switch:
                button_switch[event.button]()

        switch = {
            "enter": _enter,
            "exit": _exit,
            "update": self.update(_update),
            "button_pressed": _button_pressed,
        }

        if event.name in switch:
            switch[event.name]()
