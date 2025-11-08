"""
location.py contains the Item and CurrentRoom enums
"""
from enum import Enum


class Item(Enum):
    """
    The enum of items that are possible to get during the game, the default is ITEM_NOTHING
    """
    ITEM_DNS = "dns.cfg"
    ITEM_VAULT = "vault_dump.txt"
    ITEM_MALWARE = "proc_tree.jsonl"
    ITEM_SOC = "auth.log"
    ITEM_NOTHING = "no item"


class CurrentRoom(Enum):
    """
    The enum of the different rooms you can enter
    """
    BASE = 1
    SOC = 2
    DNS = 3
    VAULT = 4
    MALWARE = 5
    FINAL_GATE = 6

    @staticmethod
    def get_room_name(current_room: Enum) -> str | None:
        """
        Will get the nice printable version of the room enum passed in
        :param current_room: The room you want the name of
        :returns: The name of the room, or none if the room type is invalid
        """
        return_value = None
        match current_room:
            case CurrentRoom.BASE:
                return_value = "Lobby"
            case CurrentRoom.SOC:
                return_value = "SOC"
            case CurrentRoom.DNS:
                return_value = "DNS"
            case CurrentRoom.VAULT:
                return_value = "Vault"
            case CurrentRoom.MALWARE:
                return_value = "Malware"
            case CurrentRoom.FINAL_GATE:
                return_value = "Final Gate"
        return return_value

    @staticmethod
    def get_room_item(current_room: Enum) -> Item:
        """
        Will tell you which item is inspectable in the current room
        :param current_room: The room you want to know the item of
        :returns: The item that can be inspected, or no item if none is found
        """
        match current_room:
            case CurrentRoom.DNS:
                return Item.ITEM_DNS
            case CurrentRoom.VAULT:
                return Item.ITEM_VAULT
            case CurrentRoom.MALWARE:
                return Item.ITEM_MALWARE
            case CurrentRoom.SOC:
                return Item.ITEM_SOC
            # case CurrentRoom.FINAL_GATE:
            #    return "final_gate.txt"
        return Item.ITEM_NOTHING

    @staticmethod
    def get_use_item(current_room: Enum) -> str:
        """
        Will tell you if you can use a function in the room, only applies
        to the final gate
        :param current_room: The room you want to check the use of
        :returns: Gate or nothing
        """
        match current_room:
            case CurrentRoom.FINAL_GATE:
                return "gate"
        return "nothing"
