"""
Main escape room module, executes the game and creates the base classes
"""
import argparse
from dataclasses import dataclass
from typing import Any

from escaperoom.engine import Engine
from escaperoom.transcript import Transcript
from escaperoom.utils import Inventory, Utils


@dataclass
class Escape:
    """
    The main escape room class that launches the game, one of these will be
    created and parse the arguments and then run the game
    """

    def __init__(self, arguments):
        self.__args__ = arguments

    def run_game(self):
        """
        Uses the arguments provided to run the game, if invalid will stop
        the game
        :return: Nothing
        """
        data_folder_location, save_file_name = self._do_get_save_file_location_from_args()

        transcript = Transcript(data_folder_location)
        inventory = Inventory(transcript)
        utils = Utils(transcript, inventory, data_folder_location,
                      save_file_name)
        start_room = self.__args__.start
        if start_room is not None:
            start_room = start_room.lower().strip()

        run_game = True
        self._do_show_intro(start_room, transcript)

        engine = Engine(transcript, inventory, utils)
        auto_run = self.__args__.auto_run

        while run_game:
            if auto_run:
                engine.command("move soc")
                engine.command("inspect auth.log")
                engine.command("move dns")
                engine.command("inspect dns.cfg")
                engine.command("move vault")
                engine.command("inspect vault_dump.txt")
                engine.command("move malware")
                engine.command("inspect proc_tree.jsonl")
                engine.command("move gate")
                run_game = engine.command("use final_gate")
                auto_run = False
            else:
                if start_room is not None and start_room != "":
                    match start_room:
                        case "dns":
                            engine.command("move dns")
                        case "malware":
                            engine.command("move malware")
                        case "soc":
                            engine.command("move soc")
                        case "vault":
                            engine.command("move vault")
                        case "gate":
                            engine.command("move gate")

                next_step = input("What would you like to do?")
                transcript.append_log("What would you like to do?")
                run_game = engine.command(next_step)

    def _do_get_save_file_location_from_args(self) -> tuple[str, str]:
        """
        Parses the arguments and returns the valid data folder and save file names
        :return: A tuple of the data folder location and the save file name
        """
        data_folder_location = self.__args__.data_folder_location
        if data_folder_location is not None:
            data_folder_location = data_folder_location.lower().strip()
        if data_folder_location is None or data_folder_location == "":
            data_folder_location = "data"

        save_file_name = args.transcript
        if save_file_name is not None:
            save_file_name = save_file_name.lower().strip()
        if save_file_name is None or save_file_name == "":
            save_file_name = "run.txt"
        return data_folder_location, save_file_name

    def _do_show_intro(self, start_room: Any | None, transcript: Transcript):
        """method_name
        Shows the intro to the game and also prints some messages about
        starting hints
        :param start_room: The starting room set in the arguments,
        will only run if the start_room is empty, or intro
        :param transcript: Allows printing the details of the intro to the log
        :return: Nothing
        """
        if start_room is None or start_room == "" or start_room == "intro":
            transcript.print_message("Welcome to the escape room game")
            transcript.print_message(r"""
            ___________                                    __________                                                             
            \_   _____/ ______ ____ _____  ______   ____   \______   \ ____   ____   _____                                        
             |    __)_ /  ___// ___\\__  \ \____ \_/ __ \   |       _//  _ \ /  _ \ /     \                                       
             |        \\___ \\  \___ / __ \|  |_> >  ___/   |    |   (  <_> |  <_> )  Y Y  \
            /_______  /____  >\___  >____  /   __/ \___  >  |____|_  /\____/ \____/|__|_|  /                                      
                    \/     \/     \/     \/|__|        \/          \/                    \/                                       
                """)
            transcript.print_message("Enjoy the escape room!")
            transcript.print_message("Type quit to quit")
            transcript.print_message("Type hint for assistance")


parser = argparse.ArgumentParser(prog="Escape room",
                                 description="Group 9's escape room")
parser.add_argument("--start",
                    type=str,
                    help="If set to intro, will start the game. "
                         "If you enter a room, then the game will start "
                         "you in that room",
                    choices=["intro", "dns", "malware",
                             "soc", "vault", "gate"],
                    default="intro"
                    )
parser.add_argument("--transcript",
                    type=str,
                    help="Where to save the result to, "
                         "if not set will use run.txt",
                    default="run.txt")
parser.add_argument("--auto_run",
                    type=bool,
                    help="If set to true, will automatically run through all "
                         "rooms and try and solve them with no user input ",
                    default=False)
parser.add_argument("--data_folder_location",
                    type=str,
                    help="Where to find and save the data to, "
                         "the default is data",
                    default="data")

args = parser.parse_args()
escape = Escape(args)
escape.run_game()
