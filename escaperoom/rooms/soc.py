from escaperoom.rooms.base import BaseRoom
from escaperoom.rooms.currentroom import CurrentRoom


class SocRoom(BaseRoom):
    def __init__(self):
        super().__init__()
        self.__room = CurrentRoom.SOC

    def solve(self):
        """
        Add a method description here. Do not forget to return the result!
        :return:
        """
        print("You called solve on " + CurrentRoom.get_room_name(self.__room))
        self._add_log_to_transcript("I did something", self.__room)
