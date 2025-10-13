import re

from escaperoom.rooms.base import BaseRoom
from escaperoom.rooms.currentroom import CurrentRoom
from escaperoom.transcript import Transcript


class VaultRoom(BaseRoom):
    def __init__(self, transcript: Transcript):
        super().__init__(transcript)
        self.__room = CurrentRoom.VAULT

    def solve(self):
        """
        Add a method description here. Do not forget to return the result!
        :return:
        """

        # https://regex101.com/r/AKN3hE/2
        p = re.compile(pattern="\s*S\s*A\s*F\s*E\s*\{\s*(\d+)\s*-\s*(\d+)\s*-\s*(\d+)\s*}\s*",
                       flags=re.MULTILINE | re.IGNORECASE)
        # As I have three matching groups, will return a tuple of 3 items
        # TODO TM Open file and get data
        tuple_result = p.findall("")
        self.transcript.print_message("You called solve on " + CurrentRoom.get_room_name(self.__room))
        self._add_log_to_transcript("I did something", self.__room)
