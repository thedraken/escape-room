"""
utils.py holds the Utils and inventory classes and their associated methods.
"""
import json

from escaperoom.location import CurrentRoom, Item
from escaperoom.transcript import Transcript


class Inventory:
    """
    The inventory class, where you can update the player's items.
    The class also manages checking if the player's
    inventory is missing any items.
    """

    def __init__(self, transcript: Transcript):
        self.inventory_dict = {
            Item.ITEM_DNS: "",
            Item.ITEM_VAULT: "",
            Item.ITEM_MALWARE: "",
            Item.ITEM_SOC: ""
        }
        self.__transcript = transcript

    def update_inventory(self, item_type: Item, value: str | None):
        """
        Set the token received from the room the player just solved.
        :param item_type: A value from the enum Item
        :param value: The token for the value, can be empty or none as well
        :return: Nothing
        """
        if value is not None:
            self.inventory_dict[item_type] = value
        else:
            self.inventory_dict[item_type] = ""

    def get_token_name_from_item(self, item_type: Item) -> str:
        """
        Will convert the item type enum into a human-readable token name
        :param item_type: The item_type enum to convert to the token name
        :return: Returns the token name, if not valid then None is returned.
        """
        return_value = "None"
        match item_type:
            case Item.ITEM_DNS:
                return_value = "DNS"
            case Item.ITEM_VAULT:
                return_value = "SAFE"
            case Item.ITEM_MALWARE:
                return_value = "PID"
            case Item.ITEM_SOC:
                return_value = "KEYPAD"
        return return_value

    def print_inventory(self):
        """
        Checks the player's inventory and prints out the tokens
        received from the room.
        :return: Nothing
        """
        count_of_items = 0
        for item in self.inventory_dict.items():
            key = item[0]
            value = item[1]
            if value is not None and value != "":
                count_of_items += 1
                self.__transcript.print_message(
                    ":".join((self.get_token_name_from_item(key), value)))
        if count_of_items == 0:
            self.__transcript.print_message("Nothing in your inventory.")

    def get_inventory_item(self, item_type: Item) -> str:
        """
        Returns the value the item key stores from the inventory
        """
        return self.inventory_dict[item_type]

    def is_inventory_complete(self):
        """
        Checks if the player's inventory is complete with all puzzles solved,
        not necessarily correctly.
        :return: boolean if the player's inventory is complete
        """
        count_of_items = 0
        for item in self.inventory_dict.items():
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
        for item in self.inventory_dict.items():
            key = item[0]
            value = item[1]
            if value is None or value == "":
                if len(missing_items) > 0:
                    missing_items += ", "
                missing_items += self.get_token_name_from_item(key)
                count_of_items += 1
        if count_of_items == 0:
            self.__transcript.print_message("ALl items collected.")
        else:
            self.__transcript.print_message(missing_items)


class Utils:
    """
    Utils class holds several functions that could be used by other classes.
    The current list are:
    save, load, convert_to_float, and open_file
    """
    def __init__(self, transcript: Transcript,
                 inventory_to_create : Inventory,
                 save_file_path: str) -> None:
        self._transcript = transcript
        self._inventory = inventory_to_create
        self.__save_file_path__ = save_file_path

    def save(self) -> bool:
        """
        Saves the current progress of the game to a save.json file
        :return: Returns true if it successfully saved the current state
        """
        self._transcript.print_message("Saving progress...")
        try:
            transcript_dict = self._transcript.transcript_dict
            new_transcript_dict = {}
            for item in transcript_dict:
                # Because the current room key is not a string, this
                # throws json.dumps off,
                # we have to manually create a new dict type and convert it...
                string_key = str(item)
                new_transcript_dict[string_key] = transcript_dict[item]
            new_item_dict = {}
            for item in self._inventory.inventory_dict:
                string_invt_key = str(item)
                new_item_dict[string_invt_key] = self._inventory.inventory_dict[item]
            save_dict = {"transcript": new_transcript_dict, "item": new_item_dict}
            with (Transcript.open_file("save.json", self.__save_file_path__, "w")
                  as save_file):
                save_file.write(json.dumps(save_dict))
            self._transcript.print_message("Progress saved.")
            return True
        except (FileNotFoundError, FileExistsError, EOFError, KeyError,
                OSError, SystemError, TypeError, UnicodeError,
                UnicodeEncodeError, ValueError) as e:
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
            with (Transcript.open_file("save.json", self.__save_file_path__, "r")
                  as save_file):
                data = json.load(save_file)
                success_load = True
                for upper_key in data.keys():
                    for key in data[upper_key].keys():
                        if upper_key == "transcript":
                            self._update_transcript_from_load(key,
                                                              data[
                                                                  upper_key])
                        elif upper_key == "item":
                            self._update_inventory_from_load(key,
                                                             data[
                                                                 upper_key])
                        else:
                            self._transcript.print_message("Invalid save "
                                                           "file due to bad "
                                                           "key: "
                                                           f"{upper_key}.")
                            success_load = False
                if success_load:
                    self._transcript.print_message("Progress loaded.")
                else:
                    self._transcript.print_message("Error loading save file.")
                return success_load
        except (FileExistsError, FileNotFoundError, SystemError,
                OSError, EOFError, UnicodeDecodeError, UnicodeEncodeError,
                UnicodeError) as e:
            self._transcript.print_message("Error loading save file: "
                                           + str(e))
        return False

    def _update_transcript_from_load(self, room_key, json_data):

        room_keys = [member.name for member in CurrentRoom]
        string_value = json_data[room_key]
        new_key = room_key.replace("CurrentRoom.", "")
        if new_key in room_keys:
            current_room = CurrentRoom[new_key]
            self._transcript.transcript_dict.update({
                current_room: string_value})
        else:
            self._transcript.print_message("The key " +
                                           room_key
                                           + " is not a valid room")
    def _update_inventory_from_load(self, item_key, json_data):
        item_keys = [member.name for member in Item]
        string_value = json_data[item_key]
        new_key = item_key.replace("Item.", "")
        if new_key in item_keys:
            item_to_update = Item[new_key]
            self._inventory.inventory_dict.update({item_to_update: string_value})
        else:
            self._transcript.print_message("The key " + item_key
                                           + " is not a valid item")


    def convert_to_float(self, value: str) -> float | None:
        """
        Converts a string value into a float
        :param value: The string value to convert
        :return: The float value, or none if not applicable
        """
        try:
            return float(value)
        except (ValueError, FloatingPointError):
            self._transcript.print_message(value + " is not a valid number")
        return None
