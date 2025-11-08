"""
vault.py stores the VaultRoom class, for solving the vault code.
"""
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
    def __init__(self, transcript: Transcript, save_file_path: str):
        super().__init__(transcript, CurrentRoom.VAULT, save_file_path)

    def solve(self) -> str | None:
        """
        Takes the vault_dump.txt file and looks for the following pattern,
        ignoring any whitespace:
        SAFE{a-b-c}
        where a + b == c and will return the list of values that match
        that amount
        :returns: a single string result, if one is found. Otherwise, None
        """
        try:
            with self.open_file() as vault_file:
                if vault_file is not None:
                    file_entry = vault_file.read()
                    tuple_result = self._extract_matching_items(file_entry)
                    results = self._check_items_match_rule(tuple_result)
                    return self._check_results(results)
        except (ArithmeticError, AttributeError, IndexError, KeyError,
                NameError) as e:
            self.transcript.print_message("An error occurred:\n" + str(e))
        return None

    # noinspection PyMethodMayBeStatic
    def _extract_matching_items(self, file_entry: str) -> dict[str,
        tuple[str, str, str]]:
        """
        Takes the string extracted from the vault_dump.txt file and checks
        it against a regex that matches
        the condition SAFE{a-b-c} with any whitespace.
        Also ignores case sensitivity.
        :param file_entry: The string to check for the correct pattern
        :returns: A dictionary of any entries of a, b, and c where
        the valid regex is matched and the key is the actual text pulled
        from the file
        """
        p = re.compile(
            pattern=r"(\s*S\s*A\s*F\s*E\s*\{\s*(\d+)\s*-\s*(\d+)\s*-"
                    r"\s*(\d+)\s*}\s*)",
            flags=re.IGNORECASE | re.MULTILINE)
        # https://regex101.com/r/AKN3hE/2
        # As I have three matching groups, will return a collection of 3 items
        list_of_tuple_results = p.findall(file_entry)
        dict_results = {}

        for item in list_of_tuple_results:
            if len(item) == 4:
                dict_results[item[0]] = (item[1], item[2], item[3])
            else:
                self.transcript.print_message("The items in " + str(item) +
                                              " do not have 4 parts to it")
        return dict_results

    def _check_items_match_rule(self,
                                dictionary: dict[str, tuple[str, str, str]]) \
            -> dict[str, tuple[str, str, str]]:
        """
        For all items in the dictionary, do a check against the tuple and
        if a + b == c, if so, return them
        :param dictionary: The dictionary of strings to check, each item must have a
        key of the original string and a value tuple of length 3
        :returns: The dictionary of valid items where a + b = c, or
        item[0] + item[1] == item[2] of the value tuple
        """
        # We will add all matching results to the dictionary
        results = {}
        for key, value in dictionary.items():
            if len(value) == 3:
                value1 = Utils.convert_to_float(value[0])
                value2 = Utils.convert_to_float(value[1])
                value3 = Utils.convert_to_float(value[2])
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
                        "The values " + str(key) + " are valid")
                    results[key] = value
                # else:
                # self._transcript.print_message("The values "
                # + str(item) + " do not add up")
            # else:
            # self._transcript.print_message("The values " +
            # str(item) + " are invalid due to bad length")
        return results

    def _check_results(self, results: dict[str, tuple[str, str, str]]) \
            -> (str |None):
        """
        If only one result is found, create the valid string to add to run.txt,
        otherwise do nothing.
        :param results: The results to check and confirm only one data point
        has been found
        :returns: The single matching token, otherwise None
        """
        if len(results) != 0:
            # We have at least one result, let's handle it
            self.transcript.print_message(
                "The results of vault are: " + str(results))
            if len(results) == 1:
                first_key = list(results.keys())[0]
                first_value = results[first_key]
                self.add_log_to_transcript(
                    f"TOKEN[SAFE]={first_value[0]}-{first_value[1]}-{first_value[2]}")
                self.add_log_to_transcript(
                    f"EVIDENCE[SAFE].MATCH={first_key.strip()}")
                self.add_log_to_transcript(
                    f"EVIDENCE[SAFE].CHECK={first_value[0]}+{first_value[1]}"
                    f"={first_value[2]}")
                token = "-".join(first_value)
                self.transcript.print_message(
                    f"Returning token: {token}")
                return token
            self.transcript.print_message(
                "Too many tokens found, not returning any data")
            return None
        self.transcript.print_message("Vault was not solved")
        return None
