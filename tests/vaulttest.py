"""
Contains the VaultTest class
"""
import unittest
from unittest.mock import Mock

from escaperoom.rooms.vault import VaultRoom


class VaultTest(unittest.TestCase):
    """
    A class of the individual tests to run on the Vault Room
    """

    def test_extract_matching_items(self):
        """
        Tests the method _extract_matching_items found in the Vault Room.
        Looks for a matching item that follows the pattern SAFE{a-b-c}
        where spaces are allowed in between any character and a+b=c
        :return: None
        """
        transcript_mock = Mock()
        to_test_vault = VaultRoom(transcript_mock)

        list_of_items = to_test_vault._extract_matching_items("SAFE{4-5-9}")
        self.check_items_are_valid(list_of_items, 1,
                                   '4', '5', '9')

        second_list_of_items = to_test_vault._extract_matching_items(
            "S AF E{"
            "1 - 2- 3 } \n"
            "SAF3{4-5-9}\n"
            "S A F E { 1 - 2 - 4")
        self.check_items_are_valid(second_list_of_items, 1,
                                   '1', '2', '3')

    def check_items_are_valid(self, list_of_items: list[str],
                              length_of_list: int, result_a: str,
                              result_b: str,
                              result_c: str) -> None:
        assert len(list_of_items) == length_of_list
        tuple_to_check = list_of_items[0]
        assert len(tuple_to_check) == 3
        assert tuple_to_check[0] == result_a
        assert tuple_to_check[1] == result_b
        assert tuple_to_check[2] == result_c
