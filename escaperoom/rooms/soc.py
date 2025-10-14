from escaperoom.rooms.base import BaseRoom
from escaperoom.rooms.currentroom import CurrentRoom
from escaperoom.transcript import Transcript


class SocRoom(BaseRoom):
    def __init__(self, transcript: Transcript):
        super().__init__(transcript, CurrentRoom.SOC)

    def solve(self):
        """
        Add a method description here. Do not forget to return the result!
        :return:
        """
        try: # we use a try catch to open the file
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
                        continue

                self._transcript.print_message(malformed_lines_count)
                self._transcript.print_message(skipped_lines_count)

        except FileNotFoundError:
            self._transcript.print_message("File not found!!!")
            return None

        self._add_log_to_transcript(f"EVIDENCE[KEYPAD].MALFORMED_SKIPPED={malformed_lines_count}\n")

        return None
