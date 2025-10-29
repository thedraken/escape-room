"""
vault.py stores the VaultRoom class, for solving the vault code.
"""
import logging
import re

from escaperoom.location import CurrentRoom
from escaperoom.rooms.base import BaseRoom
from escaperoom.transcript import Transcript
from escaperoom.utils import Utils


class VaultRoom(BaseRoom):
    """
    Vault Room class, created for solving the vault room puzzle and returning
    the one correct string.
    Inherits the BaseRoom class and implements the solve method.
    """
    def __init__(self, transcript: Transcript):
        super().__init__(transcript, CurrentRoom.VAULT)

    def solve(self) -> str | None:
        """
        Takes the vault_dump.txt file and looks for the following pattern,
        ignoring any whitespace:
        SAFE{a-b-c}
        where a + b == c and will return the list of values that match
        that amount
        :return: a single string result, if one is found. Otherwise, None
        """
        try:
            with self.open_file() as vault_file:
                file_entry = vault_file.read()
                tuple_result = self._extract_matching_items(file_entry)
                results = self._check_items_match_rule(tuple_result)
                return self._check_results(results)
        # TODO W0718: Catching too general exception Exception (broad-exception-caught)
        except Exception as e:
            self.transcript.print_message("An error occurred:\n" + str(e))
            logging.error(e)
        return None

    # noinspection PyMethodMayBeStatic
    def _extract_matching_items(self, file_entry: str) -> list[str]:
        """
        Takes the string extracted from the vault_dump.txt file and checks
        it against a regex that matches
        the condition SAFE{a-b-c} with any whitespace.
        Also ignores case sensitivity.
        :param file_entry: The string to check for the correct pattern
        :return: A list of any entries of a, b, and c where
        the valid regex is matched
        """
        p = re.compile(
            pattern=r"\s*S\s*A\s*F\s*E\s*\{\s*(\d+)\s*-\s*(\d+)\s*-"
                    r"\s*(\d+)\s*}\s*",
            flags=re.IGNORECASE | re.MULTILINE)
        # https://regex101.com/r/AKN3hE/2
        # As I have three matching groups, will return a collection of 3 items
        tuple_result = p.findall(file_entry)
        return tuple_result

    def _check_items_match_rule(self, items: list[str]) -> list[str]:
        """
        For all items in the list, do a check if a + b == c, if so,
        return them
        :param items: The list of strings to check, each item must have a
        length of 3
        :return: The valid items where a + b = c, or
        item[0] + item[1] == item[3]
        """
        # We will add all matching results to the list
        results = []
        for item in items:
            if len(item) == 3:
                utils = Utils(self.transcript)
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
                    self.transcript.print_message(
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
        """
        If only one result is found, create the valid string to add to run.txt,
        otherwise do nothing.
        :param results: The results to check and confirm only one data point
        has been found
        :return: The single matching token, otherwise None
        """
        if len(results) != 0:
            # We have at least one result, let's handle it
            self.transcript.print_message(
                "The results of vault are: " + str(results))
            if len(results) == 1:
                item = results[0]
                self.add_log_to_transcript(
                    f"TOKEN[SAFE]={item[0]}-{item[1]}-{item[2]}")
                self.add_log_to_transcript(
                    f"EVIDENCE[SAFE].MATCH=SAFE{{{item[0]}-{item[1]}"
                    f"-{item[2]}}}")
                self.add_log_to_transcript(
                    f"EVIDENCE[SAFE].CHECK={item[0]}+{item[1]}"
                    f"={item[2]}")
                token = "-".join(item)
                self.transcript.print_message(
                    f"Returning token: {token}")
                return token
            self.transcript.print_message(
                "Too many tokens found, not returning any data")
            return None
        self.transcript.print_message("Vault was not solved")
        return None
