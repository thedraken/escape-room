"""
inventory.py holds the Item enum, and Inventory class. For manging the player's inventory and items placed in it
"""
from enum import Enum

from escaperoom.transcript import Transcript


class Item(Enum):
    """
    The enum of items that are possible to get during the game, the default is ITEM_NOTHING
    """
    ITEM_DNS = "dns.cfg"
    ITEM_VAULT = "vault_dump.txt"
    ITEM_MALWARE = "pro_tree.jsonl"
    ITEM_SOC = "auth.log"
    ITEM_NOTHING = "no item"


class Inventory:
    """
    The inventory class, where you can update the player's items. The class also manages checking if the player's
    inventory is missing any items.
    """
    def __init__(self, transcript: Transcript):
        self._inventory = {
            Item.ITEM_DNS.value: "",
            Item.ITEM_VAULT.value: "",
            Item.ITEM_MALWARE.value: "",
            Item.ITEM_SOC.value: ""
        }
        self.__transcript = transcript

    def update_inventory(self, item_type: Item, value: str | None):
        """
        Set the token received from the room the player just solved.
        :param item_type: A value from the enum Item
        :param value: The token for the value, can be empty or none as well
        :return: Nothing
        """
        self._inventory[item_type.value] = value

    def print_inventory(self):
        """
        Checks the player's inventory and prints out the tokens received from the room.
        :return: Nothing
        """
        count_of_items = 0
        for key in self._inventory.keys():
            if self._inventory[key] is not None and self._inventory[key] != "":
                count_of_items += 1
                self.__transcript.print_message(":".join((key, self._inventory[key])))
        if count_of_items == 0:
            self.__transcript.print_message("Nothing in your inventory.")

    def is_inventory_complete(self):
        """
        Checks if the player's inventory is complete with all puzzles solved, not necessarily correctly.
        :return: boolean if the player's inventory is complete
        """
        count_of_items = 0
        for key in self._inventory.keys():
            if self._inventory[key] is not None and self._inventory[key] != "":
                count_of_items += 1
        return count_of_items == 4

    def print_missing_items(self):
        """
        Prints a statement of the items the player is currently missing to use the gate.
        :return: Nothing
        """
        count_of_items = 0
        missing_items = ""
        for key in self._inventory.keys():
            if self._inventory[key] is None or self._inventory[key] == "":
                if len(missing_items) > 0:
                    missing_items += ", "
                missing_items += key
                count_of_items += 1
        if count_of_items == 0:
            self.__transcript.print_message("ALl items collected.")
        else:
            self.__transcript.print_message(missing_items)
