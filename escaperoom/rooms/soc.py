from escaperoom.rooms.base import BaseRoom
from escaperoom.rooms.currentroom import CurrentRoom
from escaperoom.transcript import Transcript
import re

class SocRoom(BaseRoom):
    def __init__(self, transcript: Transcript):
        super().__init__(transcript)
        self.__room = CurrentRoom.SOC

    def solve(self):
        """
       This method is to find the most likely attacking subnet by:
       -Going through each and every line in the auth.log file
       -Skip all malformed or NULL lines
       -Check if the valid lines have valid IP addresses
       -And then get all "Failed Password" attempts
       -Get the IP address with most failed passwords and then get its last two digits
       -Find the number of times theyve tried to attempt
       -Gte the token {LAST TWO DIGITS OF THE IP ADDRESS}{NUMBER OF TIMES TRIED}
       -Send the token and other counts to the transcripts
        """
        ip_pattern = re.compile(r'\b(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\b')

        try: # we use a try catch to open the file
            # open the auth.log file
            with open('data/auth.log', 'r') as auth_file:
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
                        continue

                    # try to find an IP address in this line
                    match = ip_pattern.search(line)

                    if match:
                        ip = match.group(1)
                        # print(ip)
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


        except FileNotFoundError:
            print("File not found!!!")
            return None

        self.transcript.print_message(f"EVIDENCE[KEYPAD].MALFORMED_SKIPPED={malformed_lines_count}")

        return None
