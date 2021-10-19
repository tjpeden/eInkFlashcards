import alarm
import board

from event import ButtonPressedEvent, Event
from state_machine import StateMachine

BUTTONS = ["A", "B", "C", "D"]

class InputManager(StateMachine):
    def __init__(self, magtag) -> None:
        super().__init__(self.start)

        self.magtag = magtag

        self._start_switch = self._create_start_switch()
        self._active_switch = self._create_active_switch()
        self._sleep_switch = self._create_sleep_switch()

    def _create_start_switch(self):
        def _start():
            print("InputManager#start: start")
            self.subscribe("update")
            self.subscribe("sleep")

            self.transition_to(self.active)

        return {
            "start": _start
        }

    def _create_active_switch(self):
        def _enter():
            print("InputManager#active: enter")
            self.magtag.init_buttons()

        def _exit():
            print("InputManager#active: exit")
            self.magtag.deinit_buttons()

        def _update():
            for i, button in enumerate(self.magtag.buttons):
                button.update()

                if button.rose:
                    self.publish(
                        ButtonPressedEvent(BUTTONS[i], long=button.last_duration >= 1),
                    )

        def _sleep():
            print("InputManager#active: sleep")
            self.transition_to(self.sleep)

        return {
            "enter": _enter,
            "exit": _exit,
            "update": _update,
            "sleep": _sleep,
        }

    def _create_sleep_switch(self):
        def _update():
            print("InputManager#sleep: update")
            buttons = (board.BUTTON_A, board.BUTTON_D)
            button_alarms = [alarm.pin.PinAlarm(pin=pin, value=False, pull=True) for pin in buttons]

            alarm.exit_and_deep_sleep_until_alarms(*button_alarms)

        return {
            "enter": lambda: print("InputManager#sleep: enter"),
            "update": _update,
        }

    def start(self, event: Event) -> None:
        self._start_switch.get(event.name, lambda: None)()

    def active(self, event: Event) -> None:
        self._active_switch.get(event.name, lambda: None)()

    def sleep(self, event: Event) -> None:
        self._sleep_switch.get(event.name, lambda: None)()
