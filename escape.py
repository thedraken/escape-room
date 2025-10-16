"""
Main escape room module, executes the game and creates the base classes
"""
import escaperoom.engine
import escaperoom.transcript

RUN_GAME = True
transcript = escaperoom.transcript.Transcript()
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

engine = escaperoom.engine.Engine(transcript)

while RUN_GAME:
    next_step = input("What would you like to do?")
    transcript.append_log("What would you like to do?")
    RUN_GAME = engine.command(next_step)
