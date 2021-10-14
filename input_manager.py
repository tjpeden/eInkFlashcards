import alarm
import board

from event import ButtonPressedEvent, Event
from state_machine import StateMachine

BUTTONS = ["A", "B", "C", "D"]

class InputManager(StateMachine):
    def __init__(self, magtag) -> None:
        super().__init__(self.start)

        self.magtag = magtag

    def start(self, event: Event) -> None:
        def _start():
            self.subscribe("update")
            self.subscribe("sleep")

            self.transition_to(self.active)

        switch = {
            "start": _start
        }

        if event.name in switch:
            switch[event.name]()

    def active(self, event: Event) -> None:
        def _enter():
            print("active: enter")
            self.magtag.init_buttons()

        def _exit():
            print("active: exit")
            self.magtag.deinit_buttons()

        def _update():
            for i, button in enumerate(self.magtag.buttons):
                button.update()

                if button.rose:
                    self.publish(
                        ButtonPressedEvent(BUTTONS[i], long=button.last_duration >= 1),
                    )

        def _sleep():
            print("active: sleep")
            self.transition_to(self.sleep)

        switch = {
            "enter": _enter,
            "exit": _exit,
            "update": _update,
            "sleep": _sleep,
        }

        if event.name in switch:
            switch[event.name]()

    def sleep(self, event: Event) -> None:
        def _update():
            print("sleep: update")
            buttons = (board.BUTTON_A, board.BUTTON_D)
            button_alarms = [alarm.pin.PinAlarm(pin=pin, value=False, pull=True) for pin in buttons]

            alarm.exit_and_deep_sleep_until_alarms(*button_alarms)

        switch = {
            "enter": lambda: print("sleep: enter"),
            "update": _update,
        }

        if event.name in switch:
            switch[event.name]()
