"""
transcript.py holds the Transcript class object
"""
import datetime
import locale
import os
from typing import Any, IO

from escaperoom.location import CurrentRoom


class Transcript:
    """
    Transcript class involves methods for adding details to the logs,
    this can be both the chronological log
    and the run.txt file, depending on the method called.
    """
    def __init__(self, folder_path: str):
        self.transcript_dict = {
            CurrentRoom.BASE: "",
            CurrentRoom.SOC: "",
            CurrentRoom.DNS: "",
            CurrentRoom.VAULT: "",
            CurrentRoom.MALWARE: "",
            CurrentRoom.FINAL_GATE: ""
        }
        self.transcript_crono_order = ""
        self.__folder_path__ = folder_path

    def append(self, transcript_text, current_room: CurrentRoom):
        """
        Appends the transcript text to the transcript log file
        :param transcript_text: The log to append
        :param current_room: The room the transcript action was for
        :return: NONE
        """
        transcript_value = self.transcript_dict.get(current_room)
        transcript_value += transcript_text + "\n"
        self.transcript_dict.update({current_room: str(transcript_value)})
        current_room_name = CurrentRoom.get_room_name(current_room)
        if current_room_name is None:
            current_room_name = "Unknown"
        self.append_log(current_room_name + ": " + transcript_text)

    def append_log(self, log_text):
        """
        Logs an action, but does not attach to the run.txt file for submission
        The log is appended with the current date time
        :param log_text: The log text to add
        :return: NONE
        """
        # Set correct format, otherwise we get American dates...
        locale.setlocale(locale.LC_ALL, "en_GB.UTF-8")
        self.transcript_crono_order += (datetime.datetime.now().strftime("%x %X")
                                        + " - "
                                        + log_text + "\n")

    def print_message(self, message):
        """
        Prints a message to the console, will also add it to the chronological log
        :param message: The message to print
        :return: Nothing
        """
        print(str(message))
        self.append_log(str(message))

    def save_transcript(self, save_file_name: str):
        """
        Will save both the specified transcript file and the chronological
        log to file, ready for a user to browse.
        :return: Nothing
        """
        try:
            with (self.open_file("transcript_crono.txt", self.__folder_path__, "w") as
                  transcript_file):
                transcript_file.write(self.transcript_crono_order)
        except (FileNotFoundError, OSError, EOFError, FileExistsError,
                SystemError) as e:
            print(f"An error occurred writing the file: {e}")
        try:
            with self.open_file(save_file_name, self.__folder_path__, "w") as transcript_file:
                for item in self.transcript_dict:
                    transcript_file.write(str(self.transcript_dict.get(item)))
        except (FileNotFoundError, OSError, EOFError, FileExistsError,
                SystemError) as e:
            print(f"An error occurred writing the file: {e}")

    @staticmethod
    def open_file(filename: str, folder: str = "data", mode: str = "r") \
            -> IO[Any]:
        """
        Opens a file on the device, it does assume the file is one folder
        deep from the current working directory
        :param folder: The folder the file is in, the default is the
        data directory
        :param filename: The name of the file to open
        :param mode: The mode of how to open the file, for a list of
        valid parameters,
        check method builtins.open.
        At time of writing, and for the current Python library used, they are:
        ========= =============================================================
        Character Meaning
        --------- -------------------------------------------------------------
        'r'       open for reading (default)
        'w'       open for writing, truncating the file first
        'x'       create a new file and open it for writing
        'a'       open for writing, appending to the end of the file
                    if it exists
        'b'       binary mode
        't'       text mode (default)
        '+'       open a disk file for updating (reading and writing)
        'U'       universal newline mode (deprecated)
        ========= =============================================================
        :return: A file stream for various types,
                 depending on the mode selected
        """
        return open(file=os.sep.join([folder, filename]), mode=mode,
                    encoding="utf-8")
