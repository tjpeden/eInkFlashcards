from event import Event, EnterEvent, ExitEvent

class StateMachine:
    _subscriptions = {}

    def __init__(self, start) -> None:
        self._state = start
        self._next = start

    def subscribe(self, name: str) -> None:
        if name not in self._subscriptions:
            self._subscriptions[name] = []

        self._subscriptions[name].append(self)

    @classmethod
    def publish(self, event: Event) -> None:
        if event.name in self._subscriptions:
            for machine in self._subscriptions[event.name]:
                machine.dispatch(event)

    def transition_to(self, state) -> None:
        self._next = state

    def dispatch(self, event: Event) -> None:
        self._state(event)

        if self._state != self._next:
            self._state(ExitEvent())

            self._state = self._next

            self._state(EnterEvent())
