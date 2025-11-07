# pylint: disable=protected-access
# We disable this check in unit test classes, we want to access protected
# methods to test them, but do not want them to be made public for others
# to use incorrectly
"""
Contains the VaultTest class
"""
import unittest
from unittest.mock import Mock

from escaperoom.rooms.vault import VaultRoom
from escaperoom.utils import Utils


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
        to_test_vault = self.create_test_vault()

        list_of_items = to_test_vault._extract_matching_items("SAFE{4-5-9}")
        self.check_items_are_valid(list_of_items, "SAFE{4-5-9}", 1,
                                   '4', '5', '9')

        second_list_of_items = to_test_vault._extract_matching_items(
            "S AF E{1 - 2- 3 } \n"
            "SAF3{4-5-9}\n"
            "S A F E { 1 - 2 - 4")
        self.check_items_are_valid(second_list_of_items,
                                   "S AF E{1 - 2- 3 } \n", 1,
                                   '1', '2', '3')

    def test_check_items_match_rule(self):
        """
        Test method for validating the behaviour of the
        `_check_items_match_rule` method.
        Checks the values that pass the rule also add up a+b=c
        Returns: Nothing
        """
        to_test_vault = self.create_test_vault()

        list_of_items_to_check = {"SAFE-4-2-3": ('4', '4', '5'),
                                  "SAFE-4-6-10": ('4', '6', '10'),
                                  "SAFE-4-4-10": ('4', '4', '10')}

        results = to_test_vault._check_items_match_rule(list_of_items_to_check)
        assert len(results) == 1
        tuple_result = results["SAFE-4-6-10"]
        assert len(tuple_result) == 3
        assert (float(tuple_result[0])
                + float(tuple_result[1])
                == float(tuple_result[2]))
        assert tuple_result[0] == '4'
        assert tuple_result[1] == '6'
        assert tuple_result[2] == '10'

    def test_check_results(self):
        """
        Test method for the _check_results, confirms the data only accepts
        one result and returns it as the correct format a-b-c
        """
        vault_to_test = self.create_test_vault()

        list_of_items_to_check = {"SAFE-4-2-3": ('4', '2', '3'),
                                  "SAFE-4-4-5": ('4', '4', '5'),
                                  "SAFE-4-4-10": ('4', '4', '10'),
                                  "SAFE-4-6-10": ('4', '6', '10')}

        result_1 = vault_to_test._check_results(list_of_items_to_check)
        assert result_1 is None
        list_of_items_to_check_2 = {"SAFE-4-6-10": ('4', '6', '10')}
        result_2 = vault_to_test._check_results(list_of_items_to_check_2)
        assert result_2 == '4-6-10'

    @staticmethod
    def create_test_vault() -> VaultRoom:
        """
        Creates an instance of the Vault with a mocked transcript file
        :return: The Vault instance
        """
        transcript_mock = Mock()
        inventory_mock = Mock()
        utils = Utils(transcript_mock, inventory_mock, "mock",
                      "mock_file_name.txt")
        to_test_vault = VaultRoom(transcript_mock, utils, "mock")
        return to_test_vault

    @staticmethod
    def check_items_are_valid(dict_of_items: dict[str, tuple[str, str, str]],
                              key: str,
                              length_of_list: int,
                              result_a: str,
                              result_b: str,
                              result_c: str) -> None:
        """
        Will check the list of tuples has the correct values in,
        needs improving to check multiple tuples though, as it currently
        only checks the first tuple in the list
        :param dict_of_items: A list of tuples, which should have 3 items
        in each tuple
        :param length_of_list: The number of items expected in the list
        :param result_a: The expected value of a in the first tuple
        :param result_b: The expected value of b in the first tuple
        :param result_c: The expected value of c in the first tuple
        :return: Nothing
        """
        assert len(dict_of_items) == length_of_list
        tuple_to_check = dict_of_items[key]
        assert len(tuple_to_check) == 3
        assert tuple_to_check[0] == result_a
        assert tuple_to_check[1] == result_b
        assert tuple_to_check[2] == result_c
