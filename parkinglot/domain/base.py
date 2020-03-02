from typing import List


class Event(object):
    pass


class EventMixin(object):
    def __init__(self):
        self._events = []

    def _add_event(self, event: Event):
        self._events.append(event)

    def pop_events(self) -> List[Event]:
        events, self._events = self._events, []
        return events
