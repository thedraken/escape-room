from escaperoom.inventory import Inventory
from escaperoom.rooms.currentroom import CurrentRoom
from escaperoom.utils import Utils


class Engine:
    def __init__(self, transcript):
        self.current_location = CurrentRoom.BASE
        self.transcript = transcript
        self.inventory = Inventory(transcript)

    def command(self, command) -> bool:
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
        self.transcript.append_log("User called " + command)
        match command.lower():
            case "quit":
                return self.__do_quit()
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
            case _:
                self.transcript.print_message(
                    "Unknown command: " + str(command) + ", type hint to see a list of available commands")
        return True

    def __do_quit(self) -> bool:
        self.transcript.print_message("Thank you for playing")
        self.transcript.save_transcript()
        return False

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
            if item == CurrentRoom.get_room_item(self.current_location).value:
                is_valid = True
        if is_valid:
            try:
                match self.current_location:
                    case CurrentRoom.SOC:
                        from escaperoom.rooms.soc import SocRoom
                        soc_room = SocRoom(self.transcript)
                        self.inventory.update_inventory(CurrentRoom.get_room_item(self.current_location),
                                                        soc_room.solve())
                    case CurrentRoom.DNS:
                        from escaperoom.rooms.dns import DNSRoom
                        dns_room = DNSRoom(self.transcript)
                        self.inventory.update_inventory(CurrentRoom.get_room_item(self.current_location),
                                                        dns_room.solve())
                    case CurrentRoom.MALWARE:
                        from escaperoom.rooms.malware import MalwareRoom
                        malware_room = MalwareRoom(self.transcript)
                        self.inventory.update_inventory(CurrentRoom.get_room_item(self.current_location),
                                                        malware_room.solve())
                    case CurrentRoom.VAULT:
                        from escaperoom.rooms.vault import VaultRoom
                        vault_room = VaultRoom(self.transcript)
                        self.inventory.update_inventory(CurrentRoom.get_room_item(self.current_location),
                                                        vault_room.solve())
            except Exception as e:
                self.transcript.print_message("An error occurred in solving the room:")
                self.transcript.print_message(e)
        else:
            self.transcript.print_message(
                "Please enter an item with the inspect command, you are in "
                + CurrentRoom.get_room_name(self.current_location)
                + " and can inspect "
                + CurrentRoom.get_room_item(self.current_location).value)

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
            self.transcript.print_message(
                "Please enter a room with the move command, possible rooms are dns, malware, soc, vault, gate, and lobby E.g. move dns")
        else:
            self.transcript.print_message(f"You have entered into {self.current_location}")

    def __do_look(self):
        """
        Prints details about the current room the user is in
        :return: Nothing
        """
        match self.current_location:
            case CurrentRoom.BASE:
                self.transcript.print_message(
                    "You are in the lobby, you can move to any room from here. Where would you like to go?")
            case CurrentRoom.SOC:
                self.transcript.print_message(
                    "You are in the SOC room, there is a triage desk with a large file of SSH logs, called auth.log, "
                    "that show authentication attempts. Your task is to identify the most likely attacking subnet.")
            case CurrentRoom.MALWARE:
                self.transcript.print_message(
                    "You are in the Malware lab, there is a JSON-line file, called proc_tree.jsonl, that shows a process "
                    "tree containing a malicious chain ending with an exfil command.")
            case CurrentRoom.VAULT:
                self.transcript.print_message(
                    "You are in the Vault, there is a text dump lying on the table. Inside, there should be a valid "
                    "SAFE{a-b-c} code which satisfies a+b=c. Can you find it?")
            case CurrentRoom.DNS:
                self.transcript.print_message(
                    "You are in the DNS room, inside is a config file which stores items as a key value pair. "
                    "Can you find the token_tag with the hintX value to get the correct key value pair?")
            case CurrentRoom.FINAL_GATE:
                self.transcript.print_message(
                    "The final gate stands before you, have you collected all the pieces to exit the gate?")

    def __do_use(self, use):
        """

        :param use:
        :return:
        """
        # TODO TM Implement
        pass

    def __do_inventory(self):
        """
        Prints a list of items you have in your inventory, these are tokens you have got for solving rooms
        :return: Nothing
        """
        self.transcript.print_message("You currently have the following items in your inventory:")
        self.inventory.print_inventory()

    def __do_hint(self):
        """
        Prints a list of commands the user can currently do
        :return: Nothing
        """
        self.transcript.print_message("look: Allows you to look in the current room and see what is available")
        self.transcript.print_message(
            "move <room>: Allows you to move to a room to solve, rooms available are: dns, malware, soc, vault, gate, and lobby")
        self.transcript.print_message(
            "inspect <item>: Allows you to inspect an item in the room. You are currently in "
            + CurrentRoom.get_room_name(self.current_location)
            + " and can inspect " + CurrentRoom.get_room_item(self.current_location).value)
        self.transcript.print_message(
            "use <item>: Depending on the room you are in, you can use an item to do an action. You are currently in "
            + CurrentRoom.get_room_name(self.current_location)
            + " and can use " + CurrentRoom.get_use_item(self.current_location))
        self.transcript.print_message("inventory: Prints a list of all items found your inventory")
        self.transcript.print_message(
            "save: Saves the progress of your current game to a file in the data folder, called save.txt")
        self.transcript.print_message(
            "load: If a save.txt file is found and it is valid, will load it and set that as your current progress. "
            "Will overwrite any progress already done in this session")
        self.transcript.print_message(
            "quit: Exits the game and prints currently collected evidence to a transcript file")
        self.transcript.print_message("hint: Gives a list of available commands")

    def __do_save(self):
        """
        Saves the current state of the game
        :return: Nothing
        """
        utils = Utils(self.transcript)
        if utils.save():
            self.transcript.print_message("You saved the current game successfully")
        else:
            self.transcript.print_message("You did not save the current game successfully")

    def __do_load(self):
        """
        Loads the current state of the game from a save.txt file
        :return: Nothing
        """
        utils = Utils(self.transcript)
        if utils.load():
            self.transcript.print_message("You loaded the current game successfully")
        else:
            self.transcript.print_message("You did not load the current game successfully")
