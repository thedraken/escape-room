from escaperoom.engine import CurrentRoom
from escaperoom.rooms.base import BaseRoom


class DNSRoom(BaseRoom):
    def __init__(self):
        super().__init__()
        pass

    def solve(self):
        print("do something")
        self._add_log_to_transcript("I did something", CurrentRoom.DNS)
        pass
