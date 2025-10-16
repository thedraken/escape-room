import re

from escaperoom.rooms.base import BaseRoom
from escaperoom.rooms.currentroom import CurrentRoom
from escaperoom.transcript import Transcript


class VaultRoom(BaseRoom):
    def __init__(self, transcript: Transcript):
        super().__init__(transcript, CurrentRoom.VAULT)
        self.__room = CurrentRoom.VAULT

    def solve(self):
        """
        Takes the vault_dump.txt file and looks for the following pattern, ignoring any whitespace:
        SAFE{a-b-c}
        where a + b = c and will return the list of values that match that amount
        :return: the list of values that meet the expected rules for the room
        """
        try:
            with self.open_file() as vault_file:
                file_entry = vault_file.read()
                p = re.compile(pattern="\s*S\s*A\s*F\s*E\s*\{\s*(\d+)\s*-\s*(\d+)\s*-\s*(\d+)\s*}\s*",
                               flags=re.IGNORECASE | re.MULTILINE)
                # https://regex101.com/r/AKN3hE/2
                # As I have three matching groups, will return a tuple of 3 items
                tuple_result = p.findall(file_entry)
                # We will add all matching results to the list
                results = []
                for tup in tuple_result:
                    if len(tup) == 3:
                        from escaperoom.utils import Utils
                        utils = Utils(self._transcript)
                        value1 = utils.convert_to_float(tup[0])
                        value2 = utils.convert_to_float(tup[1])
                        value3 = utils.convert_to_float(tup[2])
                        if value1 is None or value2 is None or value3 is None:
                            # self._transcript.print_message("The provided values are not a float: " + str(tup))
                            # Bad values that are not numbers, continue to the next set
                            continue
                        elif value1 + value2 == value3:
                            # These values work for what we needed, add them to our results
                            self._transcript.print_message("The values " + str(tup) + " are valid")
                            results.append(tup)
                        # else:
                        # self._transcript.print_message("The values " + str(tup) + " do not add up")
                    # else:
                    #self._transcript.print_message("The values " + str(tup) + " are invalid due to bad length")
                if len(results) != 0:
                    # We have at least one result, let's handle it
                    self._transcript.print_message("The results of vault are: " + str(results))
                    for item in results:
                        self._add_log_to_transcript(f"TOKEN[SAFE]={item[0]}-{item[1]}-{item[2]}\n")
                        self._add_log_to_transcript(f"EVIDENCE[SAFE].MATCH=SAFE{{{item[0]}-{item[1]}-{item[2]}}}\n")
                        self._add_log_to_transcript(f"EVIDENCE[SAFE].CHECK={item[0]}+{item[1]}={item[2]}\n")
                    return results
                else:
                    self._transcript.print_message("Vault was not solved")
                    return None
        except Exception as e:
            self._transcript.print_message("An error occurred:\n" + str(e))
