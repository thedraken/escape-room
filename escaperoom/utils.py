"""
utils.py holds the Utils class and its associated methods.
"""
import json
import os
from typing import Any, IO

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
                # Because the current room key is not a string, this throws json.dumps off,
                # we have to manually create a new dict type and convert it...
                string_key = str(item)
                new_dict[string_key] = transcript_dict[item]
                count += 1
            with Utils.open_file("save.json", "data", "w") as save_file:
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
            with Utils.open_file("save.json", "data", "r") as save_file:
                data = json.load(save_file)
                keys = [member.name for member in CurrentRoom]
                for key in data.keys():
                    string_value = data[key]
                    new_key = key.replace("CurrentRoom.", "")
                    if new_key in keys:
                        current_room = CurrentRoom[new_key]
                        self._transcript.transcript_dict[current_room] = string_value
                    else:
                        self._transcript.print_message("The key " + key + " is not a valid room")
                self._transcript.transcript_dict = data
                self._transcript.print_message("Progress loaded.")
                return True
        except Exception as e:
            self._transcript.print_message("Error loading save file: " + str(e))
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

    @staticmethod
    def open_file(filename: str, folder: str = "data", mode: str = "r") -> IO[Any]:
        """
        Opens a file on the device, it does assume the file is one folder deep from the current working directory
        :param folder: The folder the file is in, the default is the data directory
        :param filename: The name of the file to open
        :param mode: The mode of how to open the file, for a list of valid parameters,
        check method builtins.open.
        At time of writing, and for the current Python library used, they are:
        ========= ===============================================================
        Character Meaning
        --------- ---------------------------------------------------------------
        'r'       open for reading (default)
        'w'       open for writing, truncating the file first
        'x'       create a new file and open it for writing
        'a'       open for writing, appending to the end of the file if it exists
        'b'       binary mode
        't'       text mode (default)
        '+'       open a disk file for updating (reading and writing)
        'U'       universal newline mode (deprecated)
        ========= ===============================================================
        :return: A file stream for various types, depending on the mode selected
        """
        return open(os.sep.join([folder, filename]), mode)


class Inventory:
    """
    The inventory class, where you can update the player's items. The class also manages checking if the player's
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
        Checks the player's inventory and prints out the tokens received from the room.
        :return: Nothing
        """
        count_of_items = 0
        for key in self.inventory.keys():
            if self.inventory[key] is not None and self.inventory[key] != "":
                count_of_items += 1
                self.__transcript.print_message(":".join((key, self.inventory[key])))
        if count_of_items == 0:
            self.__transcript.print_message("Nothing in your inventory.")

    def is_inventory_complete(self):
        """
        Checks if the player's inventory is complete with all puzzles solved, not necessarily correctly.
        :return: boolean if the player's inventory is complete
        """
        count_of_items = 0
        for key in self.inventory.keys():
            if self.inventory[key] is not None and self.inventory[key] != "":
                count_of_items += 1
        return count_of_items == 4

    def print_missing_items(self):
        """
        Prints a statement of the items the player is currently missing to use the gate.
        :return: Nothing
        """
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
