from abc import ABC, abstractmethod

from escaperoom.rooms.currentroom import CurrentRoom
from escaperoom.transcript import Transcript


class BaseRoom(ABC):
    def __init__(self, transcript: Transcript):
        self.transcript = transcript

    @abstractmethod
    def solve(self):
        pass

    def _add_log_to_transcript(self, log, current_room: CurrentRoom):
        if not log or not current_room:
            return
        else:
            self.transcript.append(log, current_room)