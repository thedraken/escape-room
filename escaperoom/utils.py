from escaperoom.transcript import Transcript


class Utils:
    def __init__(self, transcript: Transcript):
        self.transcript = transcript

    def save(self):
        """

        :return: Returns true if it successfully saved the current state
        """
        self.transcript.print_message("Save")
        return True

    def load(self):
        """

        :return: Returns true if it successfully loaded the save file
        """
        self.transcript.print_message("Load")
        return True

    def convert_to_float(self, value: str) -> float | None:
        try:
            return float(value)
        except ValueError:
            self.transcript.print_message(value + " is not a valid number")
        return None
