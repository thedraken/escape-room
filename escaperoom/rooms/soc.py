"""
Room 2-SOC Triage Desk (file: auth.log )
The SSH logs show repeated authentication failures. This room identifies the most likely attacking subnet
"""
import re
from typing import AnyStr
from IPython.terminal.shortcuts.auto_suggest import accept_or_jump_to_end

from escaperoom.location import CurrentRoom
from escaperoom.rooms.base import BaseRoom
from escaperoom.transcript import Transcript


# method to check if line is malformed or not
def is_malformed_line(line):
    if not line:  # check if line is NULL
        return True

    if "Failed password" not in line and "Accepted password" not in line:  # check if line has given phrases
        return True
    return False


class SocRoom(BaseRoom):
    def __init__(self, transcript: Transcript):
        super().__init__(transcript, CurrentRoom.SOC)

    def solve(self):
        """
    This method is to find the most likely attacking subnet by:
       -Going through each and every line in the auth.log file
       -Skip all malformed lines
       -Check if the valid lines have valid IP addresses
       -And then get all "Failed Password" attempts
       -Group the first three octets(/subnet) of all the IP addresses
       -Out of which we need to find the most frequent subnet and find all the IP addresses of this subnet
       -Choose the IP that occurred most frequently and get its last octet{L}
       -Find the number of times that frequent subnet tried to attempt {COUNT}
       -Get the token {L}{COUNT}
       -Send the token and other counts to the transcript
        """

        ip_pattern = re.compile(r'\b(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\b')
        sample_lines = {}
        subnet_count = {}
        subnet_ips = {}
        ip_frequency = {}

        try:  # we use a try-except to handle exceptions with opening the file
            with self.open_file() as auth_file:  # open the auth.log file
                malformed_lines_count = 0
                accepted_lines_count = 0
                # read file line by line
                for line in auth_file:
                    # remove extra spaces
                    line = line.strip()

                    # skip malformed lines
                    if is_malformed_line(line):
                        malformed_lines_count += 1
                        continue
                    # look for IP address in each line and split them
                    match = ip_pattern.search(line)
                    if match:
                        ip = match.group(1)
                        parts = ip.split('.')

                        is_valid = True
                        for part in parts:
                            try:
                                # Check if IP address is valid (each part must be a number between 0 and 255)
                                number = int(part)
                                if number < 0 or number > 255:
                                    is_valid = False
                                    break
                            except Exception as e:
                                # If we can't convert to number, it's invalid
                                self.transcript.print_message(f"Invalid IP address !!! {e}")
                                is_valid = False
                                break

                        if is_valid:
                            if "Failed password" in line:  # we need only the "Failed Passwords"
                                # Get the /24 subnet (first 3 numbers)
                                # "198.19.0.42" -> "198.19.0"
                                subnet = parts[0] + "." + parts[1] + "." + parts[2]

                                # Count the number of times each subnet has failed
                                if subnet in subnet_count:
                                    subnet_count[subnet] += 1
                                else:
                                    subnet_count[subnet] = 1

                                # Add this IP to the list of IPs in this subnet
                                if subnet in subnet_ips:
                                    subnet_ips[subnet].append(ip)
                                else:
                                    subnet_ips[subnet] = [ip]

                                # Save one example line from this subnet-for the transcript
                                if subnet not in sample_lines:
                                    sample_lines[subnet] = line
                            else:
                                accepted_lines_count += 1  # additionally get the "Accepted Passwords" count
                                continue
                        else:
                            # IP was invalid (like 999.999.999.999)
                            malformed_lines_count += 1
                            continue
                    else:
                        # Couldn't find any IP in this line
                        malformed_lines_count += 1
                        continue

        except FileNotFoundError:
            self.transcript.print_message("File not found!!!")
            return None

        # handling if no "Failed Passwords" are found in the file
        if len(subnet_count) == 0:
            self.transcript.print_message("[ERROR] No failed passwords found!")
            return None

        # ============================================================================
        # At this point we have completed reading the auth.log file
        # And found out all the counts and information we need from the file.

        # Finding the subnet with maximum frequency of "Failed Passwords"
        max_subnet = None
        highest_count = 0

        for subnet, each_count in subnet_count.items():
            if each_count > highest_count:
                highest_count = each_count
                max_subnet = subnet

        # Finding the IP address out of the max_subnet which Failed the most
        ips_list = subnet_ips[max_subnet]

        for ip in ips_list:
            if ip in ip_frequency:
                ip_frequency[ip] += 1
            else:
                ip_frequency[ip] = 1

        most_common_ip = None
        max_appearances = 0

        for ip, appearances in ip_frequency.items():
            if appearances > max_appearances:
                max_appearances = appearances
                most_common_ip = ip

        # Get the last octet of the IP address with maximum fails {L}
        last_octet = most_common_ip.split('.')[-1]

        # Combine: last_octet {L}+ total_count_of_the_max_subnet{COUNT}= TOKEN
        token = last_octet + str(subnet_count[max_subnet])

        # TODO: need to remove these later;just for debugging
        print(f"TOKEN[KEYPAD]={token}")
        print(f"EVIDENCE[KEYPAD].TOP24={max_subnet}")
        print(f"EVIDENCE[KEYPAD].SUBNET_COUNT={subnet_count[max_subnet]}")
        print(f"EVIDENCE[KEYPAD].IP_COUNT={ip_frequency[most_common_ip]}")
        print(f"EVIDENCE[KEYPAD].SAMPLE={sample_lines[max_subnet]}")
        print(f"EVIDENCE[KEYPAD].ACCEPTED_COUNT={accepted_lines_count}")
        print(f"EVIDENCE[KEYPAD].MALFORMED_SKIPPED={malformed_lines_count}")

        # Output results and write to the transcript
        token = f"TOKEN[KEYPAD]={token}"
        top24 = f"EVIDENCE[KEYPAD].TOP24={max_subnet}"
        sub_count = f"EVIDENCE[KEYPAD].SUBNET_COUNT={subnet_count[max_subnet]}"
        ip_count = f"EVIDENCE[KEYPAD].IP_COUNT={ip_frequency[most_common_ip]}"
        sample = f"EVIDENCE[KEYPAD].SAMPLE={sample_lines[max_subnet]}"
        accepted_count = f"EVIDENCE[KEYPAD].ACCEPTED_COUNT={accepted_lines_count}"
        malformed_skipped = f"EVIDENCE[KEYPAD].MALFORMED_SKIPPED={malformed_lines_count}"

        self.add_log_to_transcript(token)
        self.add_log_to_transcript(top24)
        self.add_log_to_transcript(sub_count)
        self.add_log_to_transcript(ip_count)
        self.add_log_to_transcript(sample)
        self.add_log_to_transcript(accepted_count)
        self.add_log_to_transcript(malformed_skipped)

        return "\n".join([token, top24, sub_count, ip_count, sample, accepted_count, malformed_skipped])
