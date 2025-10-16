import json
import os

from escaperoom.transcript import Transcript


class Utils:
    def __init__(self, transcript: Transcript):
        self.transcript = transcript

    def save(self):
        """
        Saves the current progress of the game to a save.json file
        :return: Returns true if it successfully saved the current state
        """
        self.transcript.print_message("Saving progress...")
        try:
            transcript_dict = self.transcript.transcript_dict
            new_dict = []
            for item in transcript_dict:
                string_key = str(item)
                new_dict.append([string_key, transcript_dict[item]])
            with open(os.sep.join(["data", "save.json"]), "w") as save_file:
                save_file.write(json.dumps(new_dict))
            self.transcript.print_message("Progress saved.")
            return True
        except Exception as e:
            self.transcript.print_message("Error saving progress: " + str(e))
        return False

    def load(self):
        """
        Loads the current state from the save.json file, if it exists
        Will overwrite the current state, with the data
        :return: Returns true if it successfully loaded the save file
        """
        self.transcript.print_message("Loading progress...")
        try:
            with open(os.sep.join(["data", "save.json"]), "r") as save_file:
                json_file = json.load(save_file)
                self.transcript.transcript_dict = json_file
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
