from enum import Enum
class Engine:
    def __init__(self):
        self.current_location = CurrentRoom.BASE
    def command(self, command):
        match command.lower():
            case "quit":
                print("Thank you for playing")
                return False
            case "help":
                print("look: Allows you to look in the current room and see what is available")
                print(
                    "move <room>: Allows you to move to a room to solve, rooms available are: dns, malware, soc, vault, gate, and lobby")
                print(
                    "inspect <item>: Allows you to check an item you currently have in your inventory and see what it is")
                print("use <item>: ")
                print("inventory: Prints a list of all items found your inventory")
                print("hint: Gives you a hint for your current room")
                print("save: Saves the progress of your current game to a file in the data folder, called save.txt")
                print(
                    "load: If a save.txt file is found and it is valid, will load it and set that as your current progress. Will overwrite any progress already done in this session")
                print("quit: Exits the game and prints currently collected evidence to a transcript file")
                print("help: Gives a list of available commands")
            case move if move.startswith("move"):
                is_valid = False
                commands = move.split(" ")
                if commands[0] == "move" and len(commands) > 1:
                    new_room = commands[1]
                    match new_room.lower():
                        case "dns":
                            self.current_location = CurrentRoom.DNS
                            is_valid = True
                        case "malware":
                            self.current_location = CurrentRoom.MALWARE
                            is_valid = True
                        case "soc":
                            self.current_location = CurrentRoom.SOC
                            is_valid = True
                        case "vault":
                            self.current_location = CurrentRoom.VAULT
                            is_valid = True
                        case "gate":
                            self.current_location = CurrentRoom.FINAL_GATE
                            is_valid = True
                        case "lobby":
                            self.current_location = CurrentRoom.BASE
                            is_valid = True
                if not is_valid:
                    print("Please enter a room with the move command, possible rooms are dns, malware, soc, vault, gate, and lobby E.g. move dns")
                else:
                    print(f"You have entered into {self.current_location}")
        return True
class CurrentRoom(Enum):
    BASE = 1
    SOC = 2
    DNS = 3
    VAULT = 4
    MALWARE = 5
    FINAL_GATE = 6

