import os
from abc import ABC, abstractmethod

from escaperoom.rooms.currentroom import CurrentRoom
from escaperoom.transcript import Transcript


class BaseRoom(ABC):
    def __init__(self, transcript: Transcript, current_room: CurrentRoom):
        self._transcript = transcript
        self._current_room = current_room

    @abstractmethod
    def solve(self):
        pass

    def _add_log_to_transcript(self, log):
        if not log or not self._current_room:
            return
        else:
            self._transcript.append(log, self._current_room)

    def open_file(self):
        return open(os.sep.join(["data", CurrentRoom.get_room_item(self._current_room)]), "r")
