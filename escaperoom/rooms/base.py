"""
base.py has the abstract class base room, with standard methods shared between rooms.
This includes accessing the room's file, the abstract solve, and adding a log to the transcript
"""
from abc import ABC, abstractmethod
from typing import Any, IO

from escaperoom.location import CurrentRoom
from escaperoom.transcript import Transcript


class BaseRoom(ABC):
    """
    The abstract base class that all solvable rooms must inherit from.
    """
    def __init__(self, transcript: Transcript, current_room: CurrentRoom):
        self.transcript = transcript
        self.current_room = current_room

    @abstractmethod
    def solve(self) -> str | None:
        """
        The abstract method to solve the room.
        :return: A string if a valid result is obtained, otherwise None
        """

    def add_log_to_transcript(self, log: str) -> None:
        """
        Adds the official log to the run.txt transcript, this is what we will
        be graded on so check formatting!
        :param log: The log to add
        :return: None
        """
        if not log or not self.current_room:
            return
        self.transcript.append(log, self.current_room)

    def open_file(self) -> None | IO[Any]:
        """
        Will open the file for the relevant room, if it exists
        :return: A file stream for reading, if the room has a file to open,
        otherwise None
        """
        item = CurrentRoom.get_room_item(self.current_room).value
        if item != "no item":
            return Transcript.open_file(item, "data")
        return None
