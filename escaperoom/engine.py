from escaperoom.rooms.currentroom import CurrentRoom
from escaperoom.rooms.dns import DNSRoom
from escaperoom.rooms.malware import MalwareRoom
from escaperoom.rooms.soc import SocRoom
from escaperoom.rooms.vault import VaultRoom

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
        :return: returns if the game should carry on running, if false, the game will be ended by the escape CLI
        """
        match command.lower():
            case "quit":
                print("Thank you for playing")
                return False
            case "look":
                self.__do_look()
            case move if move.startswith("move"):
                self.__do_move(move)
            case inspect if inspect.startswith("inspect"):
                self.__do_inspect(inspect)
            case use if use.startswith("use"):
                self.__do_use(use)
            case "inventory":
                self.__do_inventory()
            case "hint":
                self.__do_hint()
            case "save":
                self.__do_save()
            case "load":
                self.__do_load()
        return True

    def __do_inspect(self, inspect):
        """
        If you are in a valid location and inspect the right item, this will attempt to solve the room
        Relies on the current_room set in the engine
        :param inspect: The item to inspect
        :return: Nothing
        """
        is_valid = False
        commands = inspect.split(" ")
        if commands[0] == "inspect" and len(commands) > 1:
            item = commands[1]
            if item == CurrentRoom.get_room_item(self.current_location):
                is_valid = True
        if is_valid:
            try:
                match self.current_location:
                    case CurrentRoom.SOC:
                        soc_room = SocRoom()
                        soc_room.solve()
                    case CurrentRoom.DNS:
                        dns_room = DNSRoom()
                        dns_room.solve()
                    case CurrentRoom.MALWARE:
                        malware_room = MalwareRoom()
                        malware_room.solve()
                    case CurrentRoom.VAULT:
                        vault_room = VaultRoom()
                        vault_room.solve()
            except Exception as e:
                print("An error occurred in solving the room:")
                print(e)
        else:
            print(
                "Please enter an item with the inspect command, you are in "
                + CurrentRoom.get_room_name(self.current_location)
                + " and can inspect "
                + CurrentRoom.get_room_item(self.current_location))

    def __do_move(self, move):
        """
        Allows the user to move to a room specified, if the room is invalid also reports on it
        :param move:
        :return:
        """
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

    def __do_look(self):
        """
        Prints details about the current room the user is in
        :return: Nothing
        """
        match self.current_location:
            case CurrentRoom.BASE:
                print("You are in the lobby, you can move to any room from here. Where would you like to go?")
            case CurrentRoom.SOC:
                print("You are in the SOC room, there is a triage desk with a large file of SSH logs, called auth.log, "
                      "that show authentication attempts. Your task is to identify the most likely attacking subnet.")
            case CurrentRoom.MALWARE:
                print(
                    "You are in the Malware lab, there is a JSON-line file, called proc_tree.jsonl, that shows a process "
                    "tree containing a malicious chain ending with an exfil command.")
            case CurrentRoom.VAULT:
                print("You are in the Vault, there is a text dump lying on the table. Inside, there should be a valid "
                      "SAFE{a-b-c} code which satisfies a+b=c. Can you find it?")
            case CurrentRoom.DNS:
                print("You are in the DNS room, inside is a config file which stores items as a key value pair. "
                      "Can you find the token_tag with the hintX value to get the correct key value pair?")
            case CurrentRoom.FINAL_GATE:
                print("The final gate stands before you, have you collected all the pieces to exit the gate?")

    def __do_use(self, use):
        """

        :param use:
        :return:
        """
        pass

    def __do_inventory(self):
        """

        :return:
        """
        pass

    def __do_hint(self):
        """
        Prints a list of commands the user can currently do
        :return: Nothing
        """
        print("look: Allows you to look in the current room and see what is available")
        print(
            "move <room>: Allows you to move to a room to solve, rooms available are: dns, malware, soc, vault, gate, and lobby")
        print(
            "inspect <item>: Allows you to inspect an item in the room. You are currently in "
            + CurrentRoom.get_room_name(self.current_location)
            + " and can inspect " + CurrentRoom.get_room_item(self.current_location))
        print("use <item>: Depending on the room you are in, you can use an item to do an action. You are currently in "
              + CurrentRoom.get_room_name(self.current_location)
              + " and can use " + CurrentRoom.get_use_item(self.current_location))
        print("inventory: Prints a list of all items found your inventory")
        print("save: Saves the progress of your current game to a file in the data folder, called save.txt")
        print("load: If a save.txt file is found and it is valid, will load it and set that as your current progress. "
              "Will overwrite any progress already done in this session")
        print("quit: Exits the game and prints currently collected evidence to a transcript file")
        print("help: Gives a list of available commands")

    def __do_save(self):
        """

        :return:
        """
        pass

    def __do_load(self):
        """

        :return:
        """
        pass
