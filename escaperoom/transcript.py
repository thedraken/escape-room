import datetime

from escaperoom.rooms.currentroom import CurrentRoom
from escaperoom.utils import Utils


class Transcript:
    def __init__(self):
        self.transcript_dict = {
            CurrentRoom.BASE: "",
            CurrentRoom.SOC: "",
            CurrentRoom.DNS: "",
            CurrentRoom.VAULT: "",
            CurrentRoom.MALWARE: "",
            CurrentRoom.FINAL_GATE: ""
        }
        self.transcript_crono_order = ""

    def append(self, transcript_text, current_room: CurrentRoom):
        """
        Appends the transcript text to the transcript log file
        :param transcript_text: The log to append
        :param current_room: The room the transcript action was for
        :return: NONE
        """
        transcript_value = self.transcript_dict.get(current_room)
        transcript_value += transcript_text
        self.transcript_dict.update({current_room: transcript_value})
        self.append_log(CurrentRoom.get_room_name(current_room) + ": " + transcript_text)

    def append_log(self, log_text):
        """
        Logs an action, but does not attach to the run.txt file for submission
        The log is appended with the current date time
        :param log_text: The log text to add
        :return: NONE
        """
        self.transcript_crono_order += str(datetime.datetime.now()) + " - " + log_text + "\n"

    def print_message(self, message):
        print(str(message))
        self.append_log(str(message))

    def save_transcript(self):
        try:
            with Utils.open_file("data", "transcript_crono.txt", "w") as transcript_file:
                transcript_file.write(self.transcript_crono_order)
        except Exception as e:
            print("An error occurred writing the file:")
            print(e)
        try:
            with Utils.open_file("data", "run.txt", "w") as transcript_file:
                for item in self.transcript_dict:
                    transcript_file.write(str(self.transcript_dict.get(item)) + "\n")
        except Exception as e:
            print("An error occurred writing the file:")
            print(e)
