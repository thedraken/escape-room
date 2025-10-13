from escaperoom.rooms.base import BaseRoom
from escaperoom.rooms.currentroom import CurrentRoom
from escaperoom.transcript import Transcript


class SocRoom(BaseRoom):
    def __init__(self, transcript: Transcript):
        super().__init__(transcript)
        self.__room = CurrentRoom.SOC

    def solve(self):
        """
        Add a method description here. Do not forget to return the result!
        :return:
        """
        self.transcript.print_message("You called solve on " + CurrentRoom.get_room_name(self.__room))
        self._add_log_to_transcript("I did something", self.__room)
