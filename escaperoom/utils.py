"""
TODO TM
"""
import json
import os
from typing import Any, IO

from escaperoom.rooms.currentroom import CurrentRoom
from escaperoom.transcript import Transcript


class Utils:
    """
    TODO TM
    """
    def __init__(self, transcript: Transcript):
        self.transcript = transcript

    def save(self) -> bool:
        """
        Saves the current progress of the game to a save.json file
        :return: Returns true if it successfully saved the current state
        """
        self.transcript.print_message("Saving progress...")
        try:
            transcript_dict = self.transcript.transcript_dict
            new_dict = {}
            count = 0
            for item in transcript_dict:
                # Because the current room key is not a string, this throws json.dumps off,
                # we have to manually create a new dict type and convert it...
                string_key = str(item)
                new_dict[string_key] = transcript_dict[item]
                count += 1
            with Utils.open_file("data", "save.json", "w") as save_file:
                save_file.write(json.dumps(new_dict))
            self.transcript.print_message("Progress saved.")
            return True
        except Exception as e:
            self.transcript.print_message("Error saving progress: " + str(e))
        return False

    def load(self) -> bool:
        """
        Loads the current state from the save.json file, if it exists
        Will overwrite the current state, with the data
        :return: Returns true if it successfully loaded the save file
        """
        self.transcript.print_message("Loading progress...")
        try:
            with Utils.open_file("data", "save.json", "r") as save_file:
                data = json.load(save_file)
                keys = [member.name for member in CurrentRoom]
                for key in data.keys():
                    string_value = data[key]
                    new_key = key.replace("CurrentRoom.", "")
                    if new_key in keys:
                        current_room = CurrentRoom[new_key]
                        self.transcript.transcript_dict[current_room] = string_value
                    else:
                        self.transcript.print_message("The key " + key + " is not a valid room")
                self.transcript.transcript_dict = data
                self.transcript.print_message("Progress loaded.")
                return True
        except Exception as e:
            self.transcript.print_message("Error loading save file: " + str(e))
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
            self.transcript.print_message(value + " is not a valid number")
        return None

    @staticmethod
    def open_file(folder: str, filename: str, open_type: str = "r") -> IO[Any]:
        """
        TODO TM
        :param folder:
        :param filename:
        :param open_type:
        :return:
        """
        return open(os.sep.join([folder, filename]), open_type)
