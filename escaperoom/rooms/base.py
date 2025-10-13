from abc import abstractmethod, ABC

from escaperoom import transcript
from escaperoom.rooms.currentroom import CurrentRoom


class BaseRoom(ABC):
    def __init__(self):
        self.transcript = transcript.Transcript()

    @abstractmethod
    def solve(self):
        pass

    def _add_log_to_transcript(self, log, current_room: CurrentRoom):
        if not log or not current_room:
            return
        else:
            self.transcript.append(log, current_room)