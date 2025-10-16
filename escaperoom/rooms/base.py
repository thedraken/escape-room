from abc import ABC, abstractmethod

from escaperoom.rooms.currentroom import CurrentRoom
from escaperoom.transcript import Transcript
from escaperoom.utils import Utils


class BaseRoom(ABC):
    def __init__(self, transcript: Transcript, current_room: CurrentRoom):
        self._transcript = transcript
        self._current_room = current_room

    @abstractmethod
    def solve(self) -> str:
        pass

    def _add_log_to_transcript(self, log):
        """
        Adds the official log to the run.txt transcript, this is what we will be graded on so check formatting!
        :param log: The log to add
        :return: None
        """
        if not log or not self._current_room:
            return
        else:
            self._transcript.append(log, self._current_room)

    def open_file(self):
        """
        Will open the file for the relevant room, if it exists
        :return: A file stream for reading, if the room has a file to open, otherwise None
        """
        item = CurrentRoom.get_room_item(self._current_room).value
        if item != "no item":
            return Utils.open_file("data", item)
        return None
