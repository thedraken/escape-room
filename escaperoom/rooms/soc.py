import re

from escaperoom.rooms.base import BaseRoom
from escaperoom.rooms.currentroom import CurrentRoom
from escaperoom.transcript import Transcript


class SocRoom(BaseRoom):
    def __init__(self, transcript: Transcript):
        super().__init__(transcript, CurrentRoom.SOC)

    def solve(self):
        """
       This method is to find the most likely attacking subnet by:
       -Going through each and every line in the auth.log file
       -Skip all malformed or NULL lines
       -Check if the valid lines have valid IP addresses
       -And then get all "Failed Password" attempts
       -Group the first three octets(/subnet) of all the IP addresses
       -Out of which we need to find the most frequent subnet and find all the IP addresses of this subnet
       -Choose the IP that occurred most frequently and get its last octet{L}
       -Find the number of times that IP address tried to attempt {COUNT}
       -Get the token {L}{COUNT}
       -Send the token and other counts to the transcripts
        """
        ip_pattern = re.compile(r'\b(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\b')
        subnet_count = {}
        subnet_ips = {}

        try:  # we use a try catch to open the file
            # open the auth.log file
            with self.open_file() as auth_file:
                malformed_lines_count = 0
                skipped_lines_count = 0
                # read file line by line
                for line in auth_file:
                    # remove extra spaces
                    line = line.strip()

                    # skip empty or null lines
                    if not line:
                        malformed_lines_count += 1
                        continue

                    # this is to filter only the failed password attempts
                    if "Failed password" not in line:
                        skipped_lines_count += 1
                        continue  # this is to skip tje current line

                    # try to find an IP address in this line
                    match = ip_pattern.search(line)

                    if match:
                        ip = match.group(1)
                        parts = ip.split('.')

                        is_valid = True
                        for part in parts:
                            try:
                                number = int(part)
                                if number < 0 or number > 255:
                                    is_valid = False
                                    break
                            except:
                                is_valid = False
                                break

                        if is_valid:
                            # Get the /24 subnet (first 3 numbers)
                            # "198.19.0.42" -> "198.19.0"
                            subnet = parts[0] + "." + parts[1] + "." + parts[2]

                            # Count this failure for the subnet
                            if subnet in subnet_count:
                                subnet_count[subnet] += 1
                            else:
                                subnet_count[subnet] = 1

                            # Add this IP to the list of IPs in this subnet
                            if subnet in subnet_ips:
                                subnet_ips[subnet].append(ip)
                            else:
                                subnet_ips[subnet] = [ip]

                        else:

                            malformed_lines_count += 1

                    else:
                        # Couldn't find any IP in this line
                        malformed_lines_count += 1

                max_subnet = max(subnet_count, key=subnet_count.get)
                print(max_subnet)

                print(subnet_ips[max_subnet])


        except FileNotFoundError:
            self._transcript.print_message("File not found!!!")
            return None

        self.add_log_to_transcript(f"EVIDENCE[KEYPAD].MALFORMED_SKIPPED={malformed_lines_count}")

        return None
