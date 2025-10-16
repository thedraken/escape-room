from enum import Enum

from escaperoom.transcript import Transcript


class Item(Enum):
    ITEM_DNS = "dns.cfg"
    ITEM_VAULT = "vault_dump.txt"
    ITEM_MALWARE = "pro_tree.jsonl"
    ITEM_SOC = "auth.log"
    ITEM_NOTHING = "no item"


class Inventory:
    def __init__(self, transcript: Transcript):
        self.inventory = {
            Item.ITEM_DNS.value: "",
            Item.ITEM_VAULT.value: "",
            Item.ITEM_MALWARE.value: "",
            Item.ITEM_SOC.value: ""
        }
        self.__transcript = transcript

    def update_inventory(self, item_type: Item, value: str):
        self.inventory[item_type.value] = value

    def print_inventory(self):
        count_of_items = 0
        for key in self.inventory.keys():
            if self.inventory[key] is not None and self.inventory[key] != "":
                count_of_items += 1
                self.__transcript.print_message(":".join((key, self.inventory[key])))
        if count_of_items == 0:
            self.__transcript.print_message("Nothing in your inventory.")

    def is_inventory_complete(self):
        count_of_items = 0
        for key in self.inventory.keys():
            if self.inventory[key] is not None and self.inventory[key] != "":
                count_of_items += 1
        return count_of_items == 4

    def print_missing_items(self):
        count_of_items = 0
        missing_items = ""
        for key in self.inventory.keys():
            if self.inventory[key] is None or self.inventory[key] == "":
                if len(missing_items) > 0:
                    missing_items += ", "
                missing_items += key
                count_of_items += 1
        if count_of_items == 0:
            self.__transcript.print_message("ALl items collected.")
        else:
            self.__transcript.print_message(missing_items)
