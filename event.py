class Event:
    name = None

class StartEvent(Event):
    name = "start"

class EnterEvent(Event):
    name = "enter"

class ExitEvent(Event):
    name = "exit"

class UpdateEvent(Event):
    name = "update"

class SleepEvent(Event):
    name = "sleep"

class ButtonPressedEvent(Event):
    name = "button_pressed"

    def __init__(self, button: str, long=False) -> None:
        super().__init__()

        self.button = button
        self.long = long
