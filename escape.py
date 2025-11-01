"""
Main escape room module, executes the game and creates the base classes
"""
from escaperoom.engine import Engine
from escaperoom.transcript import Transcript
from escaperoom.utils import Inventory, Utils

#TODO Implement the following:
#Running python escape.py --start intro --transcript run.txt starts
#an interactive REPL (Read–Eval–Print Loop)

RUN_GAME = True
transcript = Transcript()
inventory = Inventory(transcript)
utils = Utils(transcript, inventory)
do_intro = True
if do_intro:
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

save_file_name = "run.txt"

engine = Engine(transcript, inventory, utils, save_file_name)

while RUN_GAME:
    next_step = input("What would you like to do?")
    transcript.append_log("What would you like to do?")
    RUN_GAME = engine.command(next_step)
