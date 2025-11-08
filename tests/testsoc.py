# pylint: disable=protected-access
# We disable this check in unit test classes, we want to access protected
# methods to test them, but do not want them to be made public for others
# to use incorrectly
"""
Contains the SocTest class for testing the SOC Triage Desk room
"""
import unittest
from unittest.mock import Mock, patch
from io import StringIO

from escaperoom.rooms.soc import SocRoom


class SocTest(unittest.TestCase):
    """
    A class of individual tests to run on the SOC Room.
    Tests the main flow of log parsing and token generation.
    """

    def test_parse_log_file_with_failed_passwords(self):
        """
        Test parsing a log file with multiple failed password attempts
        from different subnets.
        :return: None
        """
        log_data = """
        2025-08-09T12:00:25Z lab1 sshd[3234]: Failed password for root from 198.19.0.42 port 58191 protocol 2
2025-08-09T12:00:26Z lab1 sshd[3234]: Failed password for root from 198.19.0.42 port 58192 protocol 2
2025-08-09T12:00:27Z lab1 sshd[3234]: Failed password for admin from 198.19.0.50 port 58193 protocol 2
2025-08-09T12:00:28Z lab1 sshd[3234]: Failed password for root from 203.0.113.10 port 58194 protocol 2
"""
        soc_room = self.create_test_soc_room()

        with patch.object(soc_room, 'open_file', return_value=StringIO(log_data)):
            result = soc_room._parse_log_file()

        subnet_count, subnet_ips, sample_lines, accepted, malformed = result

        assert subnet_count["198.19.0"] == 3
        assert len(subnet_ips["198.19.0"]) == 3
        assert accepted == 0

    def test_parse_log_file_with_malformed_lines(self):
        """
        Test that malformed lines are counted and skipped correctly.
        :return: None
        """
        log_data = """MALFORMED LINE WITHOUT PROPER FORMAT
2025-08-09T12:00:25Z lab1 sshd[3234]: Failed password for root from 198.19.0.42 port 58191 protocol 2
2025-08-09T12:00:26Z lab1 sshd[3234]: Failed password for root from NOT_AN_IP port 58192 protocol 2
"""
        soc_room = self.create_test_soc_room()

        with patch.object(soc_room, 'open_file', return_value=StringIO(log_data)):
            result = soc_room._parse_log_file()

        subnet_count, subnet_ips, sample_lines, accepted, malformed = result

        assert malformed == 2
        assert subnet_count["198.19.0"] == 1

    def test_find_most_common_ip(self):
        """
        Test finding the most common IP among several different IPs.
        :return: None
        """
        soc_room = self.create_test_soc_room()
        ip_list = [
            "192.168.1.1",
            "192.168.1.2",
            "192.168.1.2",
            "192.168.1.3",
            "192.168.1.2"
        ]

        most_common, frequency = soc_room._find_most_common_ip(ip_list)

        assert most_common == "192.168.1.2"
        assert frequency == 3

    def test_generate_token(self):
        """
        Test token generation with IP and count.
        :return: None
        """
        soc_room = self.create_test_soc_room()
        token = soc_room._generate_token("192.168.1.42", 17)

        assert token == "4217"

    def test_solve_complete_workflow(self):
        """
        Integration test: Full solve workflow with realistic data.
        Tests the entire flow from log parsing to token generation.
        :return: None
        """
        log_data = """MALFORMED LINE
2025-08-09T12:00:25Z lab1 sshd[3234]: Failed password for root from 198.19.0.42 port 58191 protocol 2
2025-08-09T12:00:26Z lab1 sshd[3234]: Failed password for admin from 198.19.0.42 port 58192 protocol 2
2025-08-09T12:00:27Z lab1 sshd[3234]: Failed password for root from 198.19.0.42 port 58193 protocol 2
2025-08-09T12:00:28Z lab1 sshd[3234]: Failed password for root from 198.19.0.50 port 58194 protocol 2
2025-08-09T12:02:54Z lab1 sshd[3234]: Accepted password for svc from 198.51.100.201 port 45501 protocol 2
"""
        soc_room = self.create_test_soc_room()

        with patch.object(soc_room, 'open_file', return_value=StringIO(log_data)):
            token = soc_room.solve()

        # Token should be: last octet of most common IP (42) + count (4)
        assert token == "424"

    @staticmethod
    def create_test_soc_room() -> SocRoom:
        """
        Creates an instance of SocRoom with mocked dependencies.
        :return: The SocRoom instance for testing
        """
        transcript_mock = Mock()
        soc_room = SocRoom(transcript_mock, "mock")
        return soc_room



if __name__ == '__main__':
    unittest.main()
