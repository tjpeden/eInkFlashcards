import alarm

from magtag import MagTag
from event import ButtonPressedEvent, StartEvent, UpdateEvent
from app import App
from input_manager import InputManager

start = StartEvent()
update = UpdateEvent()
magtag = MagTag()
inputs = InputManager(magtag)
app = App(magtag)

app.dispatch(start)
inputs.dispatch(start)

if alarm.wake_alarm:
    if not magtag.button_inputs[0].value:
        magtag.play_tone(1046.5, 0.1)
        while not magtag.button_inputs[0].value:
            pass

        app.dispatch(ButtonPressedEvent("A"))

    if not magtag.button_inputs[3].value:
        magtag.play_tone(1046.5, 0.1)
        while not magtag.button_inputs[3].value:
            pass

        app.dispatch(ButtonPressedEvent("D"))

while True:
    # `publish` will call `dispatch` on all state machines
    # registerd for the given event
    app.publish(update)
