"""
TODO TM
"""
import unittest
from unittest.mock import Mock

from escaperoom.rooms.vault import VaultRoom


class VaultTest(unittest.TestCase):
    """
    TODO TM
    """

    # Doesn't actually work yet, runs whole project. Need to find out why
    def test__extract_matching_items(self):
        """
        TODO TM
        :return:
        """
        transcript_mock = Mock()
        to_test_vault = VaultRoom(transcript_mock)

        list_of_items = to_test_vault._extract_matching_items("SAFE{4-5-9}")
        # assert list_of_items == ["SAFE{4-5-9}"]
        # assert len(list_of_items) == 1
