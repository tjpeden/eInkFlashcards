# import alarm

from magtag import MagTag
from event import ButtonPressedEvent, StartEvent, UpdateEvent
from app import App
from input_manager import InputManager

magtag = MagTag()
inputs = InputManager(magtag)
app = App(magtag)

app.dispatch(StartEvent)
inputs.dispatch(StartEvent)

# if alarm.wake_alarm:
if not magtag.button_inputs[0].value:
    magtag.play_tone(1046.5, 0.1)

    while not magtag.buttons[0].value:
        magtag.buttons[0].update()

    app.dispatch(ButtonPressedEvent("A"))

if not magtag.button_inputs[3].value:
    magtag.play_tone(1046.5, 0.1)

    while not magtag.buttons[3].value:
        magtag.buttons[3].update()

    app.dispatch(ButtonPressedEvent("D"))

while True:
    # `publish` will call `dispatch` on all state machines
    # registerd for the given event
    app.publish(UpdateEvent)
