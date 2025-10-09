from engine import CurrentRoom


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
