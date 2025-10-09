from enum import Enum
class Engine:
    def __init__(self):
        self.current_location = CurrentRoom.BASE

    def command(self, command):
        """Checks the command passed by the user and if valid will execute it.
        :param command: A user can pass possible commands, depending on what they do, the engine game state will update. Possible commands are:
        look
        move <room>
        quit
        inspect <item>
        use <item>
        inventory
        hint
        save
        load
        help
        :return: returns if the game should carry on running, if false, the game will be ended by the escape CLI
        """
        match command.lower():
            case "quit":
                print("Thank you for playing")
                return False
            case "help":
                self.__do_help()
            case "look":
                self.__do_look()
            case move if move.startswith("move"):
                self.__do_move(move)
        return True

    def __do_look(self):
        match self.current_location:
            case CurrentRoom.BASE:
                print("You are in the lobby, you can move to any room from here. Where would you like to go?")
            case CurrentRoom.SOC:
                print(
                    "You are in the SOC room, there is a triage desk with a large file of SSH logs, called auth.log, that shows authentication attempts. Your task is to identify the most likely attacking subnet.")
            case CurrentRoom.MALWARE:
                print(
                    "You are in the Malware lab, there is a JSON-line file, called proc_tree.jsonl, that shows a process tree containing a malicious chain ending with an exfil command.")

    def __do_move(self, move):
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
            print(
                "Please enter a room with the move command, possible rooms are dns, malware, soc, vault, gate, and lobby E.g. move dns")
        else:
            print(f"You have entered into {self.current_location}")

    def __do_help(self):
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


class CurrentRoom(Enum):
    BASE = 1
    SOC = 2
    DNS = 3
    VAULT = 4
    MALWARE = 5
    FINAL_GATE = 6

