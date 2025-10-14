import os

from escaperoom.rooms.currentroom import CurrentRoom


class Transcript:
    def __init__(self):
        self.transcript_dict = {
            CurrentRoom.BASE: "",
            CurrentRoom.MALWARE: "",
            CurrentRoom.FINAL_GATE: "",
            CurrentRoom.DNS: "",
            CurrentRoom.SOC: "",
            CurrentRoom.VAULT: ""
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
        self.transcript_dict.update({current_room: transcript_text})
        self.transcript_crono_order += CurrentRoom.get_room_name(current_room) + ": " + transcript_text

    def append_log(self, log_text):
        self.transcript_crono_order += log_text + "\n"

    def print_message(self, message: str):
        print(message)
        self.append_log(message + "\n")

    def save_transcript(self):
        os.sep.join(["data", "transcript_crono.txt"])
        try:
            with open(os.sep.join(["data", "transcript_crono.txt"]), "w") as transcript_file:
                transcript_file.write(self.transcript_crono_order)
        except Exception as e:
            print("An error occurred writing the file:")
            print(e)
        try:
            with open(os.sep.join(["data", "run.txt"]), "w") as transcript_file:
                # TODO TM write to the transcript file with the dictionary properly
                transcript_file.write(str(self.transcript_dict))
        except Exception as e:
            print("An error occurred writing the file:")
            print(e)
