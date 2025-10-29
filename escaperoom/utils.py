"""
utils.py holds the Utils and inventory classes and their associated methods.
"""
import json

from escaperoom.location import CurrentRoom, Item
from escaperoom.transcript import Transcript


class Utils:
    """
    Utils class holds several functions that could be used by other classes.
    The current list are:
    save, load, convert_to_float, and open_file
    """
    def __init__(self, transcript: Transcript):
        self._transcript = transcript

    def save(self) -> bool:
        """
        Saves the current progress of the game to a save.json file
        :return: Returns true if it successfully saved the current state
        """
        self._transcript.print_message("Saving progress...")
        try:
            transcript_dict = self._transcript.transcript_dict
            new_dict = {}
            count = 0
            for item in transcript_dict:
                # Because the current room key is not a string, this
                # throws json.dumps off,
                # we have to manually create a new dict type and convert it...
                string_key = str(item)
                new_dict[string_key] = transcript_dict[item]
                count += 1
            with (Transcript.open_file("save.json", "data", "w")
                  as save_file):
                save_file.write(json.dumps(new_dict))
            self._transcript.print_message("Progress saved.")
            return True
        except Exception as e:
            self._transcript.print_message("Error saving progress: " + str(e))
        return False

    def load(self) -> bool:
        """
        Loads the current state from the save.json file, if it exists
        Will overwrite the current state, with the data
        :return: Returns true if it successfully loaded the save file
        """
        self._transcript.print_message("Loading progress...")
        try:
            with (Transcript.open_file("save.json", "data", "r")
                  as save_file):
                data = json.load(save_file)
                keys = [member.name for member in CurrentRoom]
                for key in data.keys():
                    string_value = data[key]
                    new_key = key.replace("CurrentRoom.", "")
                    if new_key in keys:
                        current_room = CurrentRoom[new_key]
                        self._transcript.transcript_dict[current_room] = string_value
                    else:
                        self._transcript.print_message("The key " + key
                                                       + "is not a valid room")
                # self._transcript.transcript_dict = data
                self._transcript.print_message("Progress loaded.")
                return True
        except Exception as e:
            self._transcript.print_message("Error loading save file: "
                                           + str(e))
        return False

    def convert_to_float(self, value: str) -> float | None:
        """
        Converts a string value into a float
        :param value: The string value to convert
        :return: The float value, or none if not applicable
        """
        try:
            return float(value)
        except ValueError:
            self._transcript.print_message(value + " is not a valid number")
        return None

class Inventory:
    """
    The inventory class, where you can update the player's items.
    The class also manages checking if the player's
    inventory is missing any items.
    """

    def __init__(self, transcript: Transcript):
        self.inventory = {
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
        self.inventory[item_type.value] = value

    def print_inventory(self):
        """
        Checks the player's inventory and prints out the tokens
        received from the room.
        :return: Nothing
        """
        count_of_items = 0
        for item in self.inventory.items():
            key = item[0]
            value = item[1]
            if value is not None and value != "":
                count_of_items += 1
                self.__transcript.print_message(
                    ":".join((key, value)))
        if count_of_items == 0:
            self.__transcript.print_message("Nothing in your inventory.")

    def is_inventory_complete(self):
        """
        Checks if the player's inventory is complete with all puzzles solved,
        not necessarily correctly.
        :return: boolean if the player's inventory is complete
        """
        count_of_items = 0
        for item in self.inventory.items():
            if item[1] is not None and item[1] != "":
                count_of_items += 1
        return count_of_items == 4

    def print_missing_items(self):
        """
        Prints a statement of the items the player is currently missing
        to use the gate.
        :return: Nothing
        """
        count_of_items = 0
        missing_items = ""
        for item in self.inventory.items():
            key = item[0]
            value = item[1]
            if value is None or value == "":
                if len(missing_items) > 0:
                    missing_items += ", "
                missing_items += key
                count_of_items += 1
        if count_of_items == 0:
            self.__transcript.print_message("ALl items collected.")
        else:
            self.__transcript.print_message(missing_items)
