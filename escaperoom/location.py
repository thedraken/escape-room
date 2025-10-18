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
    ITEM_MALWARE = "pro_tree.jsonl"
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
        :return: The name of the room, or none if the room type is invalid
        """
        match current_room:
            case CurrentRoom.BASE:
                return "Lobby"
            case CurrentRoom.SOC:
                return "SOC"
            case CurrentRoom.DNS:
                return "DNS"
            case CurrentRoom.VAULT:
                return "Vault"
            case CurrentRoom.MALWARE:
                return "Malware"
            case CurrentRoom.FINAL_GATE:
                return "Final Gate"
        return None

    @staticmethod
    def get_room_item(current_room: Enum) -> Item:
        """
        Will tell you which item is inspectable in the current room
        :param current_room: The room you want to know the item of
        :return: The item that can be inspected, or no item if none is found
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
        :return: Gate or nothing
        """
        match current_room:
            case CurrentRoom.FINAL_GATE:
                return "gate"
        return "nothing"
