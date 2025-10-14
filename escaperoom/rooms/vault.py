import os
import re

from escaperoom.rooms.base import BaseRoom
from escaperoom.rooms.currentroom import CurrentRoom
from escaperoom.transcript import Transcript


class VaultRoom(BaseRoom):
    def __init__(self, transcript: Transcript):
        super().__init__(transcript)
        self.__room = CurrentRoom.VAULT

    def solve(self):
        """
        Add a method description here. Do not forget to return the result!
        :return:
        """
        try:
            with open(os.sep.join(["data", "vault_dump.txt"]), "r") as vault_file:
                file_entry = vault_file.read()
                p = re.compile(pattern="\s*S\s*A\s*F\s*E\s*\{\s*(\d+)\s*-\s*(\d+)\s*-\s*(\d+)\s*}\s*",
                               flags=re.MULTILINE | re.IGNORECASE)
                # https://regex101.com/r/AKN3hE/2
                # As I have three matching groups, will return a tuple of 3 items
                tuple_result = p.findall(file_entry)
                results = []
                for tup in tuple_result:
                    if len(tup) == 3:
                        value1 = self.convert_to_float(tup[0])
                        value2 = self.convert_to_float(tup[1])
                        value3 = self.convert_to_float(tup[2])
                        if value1 is None or value2 is None or value3 is None:
                            self.transcript.print_message("The provided values are not a float: " + str(tup))
                            continue
                        elif value1 + value2 == value3:
                            self.transcript.print_message("The values " + str(tup) + " are valid")
                            results.append(tup)
                        else:
                            self.transcript.print_message("The values " + str(tup) + " do not add up")
                    else:
                        self.transcript.print_message("The values " + str(tup) + " are invalid due to bad length")
                if len(results) != 0:
                    self.transcript.print_message("The results of vault are: " + str(results))
                    self._add_log_to_transcript(str(results[0]), self.__room)
                    return results
                else:
                    self.transcript.print_message("Vault was not solved")
                    return None
        except Exception as e:
            self.transcript.print_message("An error occurred:\n" + str(e))

    def convert_to_float(self, value: str) -> float | None:
        try:
            return float(value)
        except ValueError:
            self.transcript.print_message(value + " is not a valid number")
        return None
