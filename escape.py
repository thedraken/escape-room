"""
Main escape room module, executes the game and creates the base classes
"""
import argparse
from escaperoom.engine import Engine
from escaperoom.transcript import Transcript
from escaperoom.utils import Inventory, Utils

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

args = parser.parse_args()


transcript = Transcript()
inventory = Inventory(transcript)
utils = Utils(transcript, inventory)
start_room = args.start
if start_room is not None:
    start_room = start_room.lower().strip()

RUN_GAME = True
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

SAVE_FILE_NAME = args.transcript
if SAVE_FILE_NAME is not None:
    SAVE_FILE_NAME = SAVE_FILE_NAME.lower().strip()
if SAVE_FILE_NAME is None or SAVE_FILE_NAME == "":
    SAVE_FILE_NAME = "run.txt"

engine = Engine(transcript, inventory, utils, SAVE_FILE_NAME)

while RUN_GAME:
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
    RUN_GAME = engine.command(next_step)
