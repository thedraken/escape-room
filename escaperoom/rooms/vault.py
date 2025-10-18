"""
TODO add docstring
"""
import re

from escaperoom.rooms.base import BaseRoom
from escaperoom.rooms.currentroom import CurrentRoom
from escaperoom.transcript import Transcript


class VaultRoom(BaseRoom):
    """
    TODO add docstring
    """
    def __init__(self, transcript: Transcript):
        super().__init__(transcript, CurrentRoom.VAULT)

    def solve(self) -> str | None:
        """
        Takes the vault_dump.txt file and looks for the following pattern,
        ignoring any whitespace:
        SAFE{a-b-c}
        where a + b = c and will return the list of values that match
        that amount
        :return: the list of values that meet the expected rules for the room
        """
        try:
            with self.open_file() as vault_file:
                file_entry = vault_file.read()
                tuple_result = self._extract_matching_items(file_entry)
                results = self._check_items_match_rule(tuple_result)
                return self._check_results(results)
        except Exception as e:
            self._transcript.print_message("An error occurred:\n" + str(e))
        return None

    def _extract_matching_items(self, file_entry: str) -> list[str]:
        p = re.compile(
            pattern=r"\s*S\s*A\s*F\s*E\s*\{\s*(\d+)\s*-\s*(\d+)\s*-"
                    r"\s*(\d+)\s*}\s*",
            flags=re.IGNORECASE | re.MULTILINE)
        # https://regex101.com/r/AKN3hE/2
        # As I have three matching groups, will return a collection of 3 items
        tuple_result = p.findall(file_entry)
        return tuple_result

    def _check_items_match_rule(self, items: list[str]) -> list[str]:
        # We will add all matching results to the list
        results = []
        for item in items:
            if len(item) == 3:
                from escaperoom.utils import Utils
                utils = Utils(self._transcript)
                value1 = utils.convert_to_float(item[0])
                value2 = utils.convert_to_float(item[1])
                value3 = utils.convert_to_float(item[2])
                if value1 is None or value2 is None or value3 is None:
                    # self._transcript.print_message("The provided
                    # values are not a float: " + str(item))
                    # Bad values that are not numbers, continue to
                    # the next set
                    continue
                if value1 + value2 == value3:
                    # These values work for what we needed, add them
                    # to our results
                    self._transcript.print_message(
                        "The values " + str(item) + " are valid")
                    results.append(item)
                # else:
                # self._transcript.print_message("The values "
                # + str(item) + " do not add up")
            # else:
            # self._transcript.print_message("The values " +
            # str(item) + " are invalid due to bad length")
        return results

    def _check_results(self, results) -> str | None:
        if len(results) != 0:
            # We have at least one result, let's handle it
            self._transcript.print_message(
                "The results of vault are: " + str(results))
            if len(results) == 1:
                item = results[0]
                self.add_log_to_transcript(
                    f"TOKEN[SAFE]={item[0]}-{item[1]}-{item[2]}\n")
                self.add_log_to_transcript(
                    f"EVIDENCE[SAFE].MATCH=SAFE{{{item[0]}-{item[1]}"
                    f"-{item[2]}}}\n")
                self.add_log_to_transcript(
                    f"EVIDENCE[SAFE].CHECK={item[0]}+{item[1]}"
                    f"={item[2]}\n")
                token = "-".join(item)
                self._transcript.print_message(
                    f"Returning token: {token}")
                return token
            self._transcript.print_message(
                "Too many tokens found, not returning any data")
            return None
        self._transcript.print_message("Vault was not solved")
        return None
