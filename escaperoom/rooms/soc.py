"""
Room 2-SOC Triage Desk (file: auth.log )
The SSH logs show repeated authentication failures.
This room identifies the most likely attacking subnet.
"""
import re
from collections import Counter, defaultdict

from escaperoom.location import CurrentRoom
from escaperoom.rooms.base import BaseRoom
from escaperoom.transcript import Transcript


def is_malformed_line(line):
    """
    Check if a log line is malformed or invalid.
    Arguments:
        line (str): The log line to check
    Returns:
        bool: True if malformed, False if valid
    """
    if not line:
        return True
    return "Failed password" not in line and "Accepted password" not in line


def is_valid_ip(ip_string):
    """
    Validate if an IP address has valid octets (0-255).
    Arguments:
        ip_string (str): The IP address to validate
    Returns:
        bool: True if valid, False otherwise
    """
    parts = ip_string.split('.')
    # validating the length of ip to be exactly 4 numbers
    if len(parts) != 4:
        return False
    # validating if the IP address is numbers between 0-255
    for part in parts:
        try:
            number = int(part)
            if not 0 <= number <= 255:
                return False
        except ValueError:
            return False
    return True


def extract_subnet(ip_address):
    """
    Extract /24 subnet from IP address.
    Arguments:
        ip_address (str): Full IP address
    Returns:
        str: First three octets (e.g., '198.19.0')
    """
    parts = ip_address.split('.')
    return '.'.join(parts[:3])


class SocRoom(BaseRoom):
    """SOC Room for analyzing authentication logs and detecting attack patterns."""

    def __init__(self, transcript: Transcript, save_file_path: str):
        super().__init__(transcript, CurrentRoom.SOC, save_file_path)
        self.ip_pattern = re.compile(r'\b(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\b')

    def _parse_log_file(self):
        """
        Parse auth.log file and extract relevant data.
        Returns:
            subnet_count, subnet_ips, sample_lines, accepted_count, malformed_count
        """
        subnet_count = Counter()
        subnet_ips = defaultdict(list)
        sample_lines = {}
        accepted_count = 0
        malformed_count = 0

        try: # we use a try-except to handle exceptions with opening the file
            with self.open_file() as auth_file: # open the auth.log file
                for line in auth_file:
                    line = line.strip() # remove extra spaces

                    if is_malformed_line(line):
                        malformed_count += 1
                        continue

                    match = self.ip_pattern.search(line)
                    if not match:
                        malformed_count += 1
                        continue

                    ip = match.group(1)
                    if not is_valid_ip(ip):
                        malformed_count += 1
                        continue

                    if "Failed password" in line:
                        subnet = extract_subnet(ip)
                        # Count the number of times each subnet has failed
                        subnet_count[subnet] += 1
                        # Add this IP to the list of IPs in this subnet
                        subnet_ips[subnet].append(ip)
                        # Save one example line from this subnet-for the transcript
                        if subnet not in sample_lines:
                            sample_lines[subnet] = line
                    else:  # "Accepted password"
                        accepted_count += 1

        except FileNotFoundError:
            self.transcript.print_message("File not found!!!")
            return None, None, None, 0, 0

        return subnet_count, subnet_ips, sample_lines, accepted_count, malformed_count


    def _find_most_common_ip(self, ip_list):
        """
        Find the most frequently occurring IP in a list.
        Arguments:
            ip_list (list): List of IP addresses
        Returns:
            tuple: (most_common_ip, frequency)
        """
        ip_frequency = Counter(ip_list)
        most_common_ip = None
        frequency = 0

        for ip, appearances in ip_frequency.items():
            if appearances > frequency:
                frequency = appearances
                most_common_ip = ip
        return most_common_ip, frequency

    def _generate_token(self, most_common_ip, subnet_count):
        """
        Generate token from IP's last octet and subnet count.
        Arguments:
            most_common_ip (str): The most frequently failing IP
            subnet_count (int): Total failures for the subnet
        Returns:
            str: Generated token
        """
        last_octet = most_common_ip.split('.')[-1]
        return last_octet + str(subnet_count)

    def _write_results_to_transcript(self, results):
        """
        Write all results to transcript.
        Arguments:
            results (dict): Dictionary containing all result data
        """
        output_lines = [
            f"TOKEN[KEYPAD]={results['token']}",
            f"EVIDENCE[KEYPAD].TOP24={results['max_subnet']}.0/24",
            f"EVIDENCE[KEYPAD].COUNT={results['subnet_count']}",
            #f"EVIDENCE[KEYPAD].IP_COUNT={results['ip_count']}",
            f"EVIDENCE[KEYPAD].SAMPLE={results['sample']}",
            #f"EVIDENCE[KEYPAD].ACCEPTED_COUNT={results['accepted_count']}",
            f"EVIDENCE[KEYPAD].MALFORMED_SKIPPED={results['malformed_count']}"
        ]

        # Debug output
        for line in output_lines:
            print(line)
            self.add_log_to_transcript(line)

        return results['token']

    def solve(self):
        """
        Find the most likely attacking subnet by analyzing auth.log.
        Returns:
            str: Formatted results with token and evidence
        """
        # Parse the log file
        parse_result = self._parse_log_file()
        if parse_result[0] is None:
            return None

        # At this point we have completed reading the auth.log file
        # And found out all the counts and information we need from the file.

        subnet_count, subnet_ips, sample_lines, accepted_count, malformed_count = parse_result

        if not subnet_count:
            self.transcript.print_message("[ERROR] No failed passwords found!")
            return None

        # Finding the subnet with maximum frequency of "Failed Passwords"
        max_subnet = None
        max_count = 0

        for subnet, each_count in subnet_count.items():
            if each_count > max_count:
                max_count = each_count
                max_subnet = subnet

        # Find most common IP within that subnet
        most_common_ip, frequency = self._find_most_common_ip(subnet_ips[max_subnet])

        # Generate token
        token = self._generate_token(most_common_ip, max_count)

        # Prepare results
        results = {
            'token': token,
            'max_subnet': max_subnet,
            'subnet_count': max_count,
            'ip_count': frequency,
            'sample': sample_lines[max_subnet],
            'accepted_count': accepted_count,
            'malformed_count': malformed_count
        }

        return self._write_results_to_transcript(results)
