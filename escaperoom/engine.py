"""
Stores the engine class and it's associated methods
"""
import re

from escaperoom.location import CurrentRoom, Item
from escaperoom.transcript import Transcript


class Engine:
    """
    The engine class for the overall game, will check the commands passed
    and will execute the relevant command.
    """

    def __init__(self, transcript, inventory, utils):
        self._current_location = CurrentRoom.BASE
        self._transcript = transcript
        self._inventory = inventory
        self._utils = utils

    def command(self, command) -> bool:
        """Checks the command passed by the user and if valid will execute it.
        :param command: A user can pass possible commands,
        depending on what they do, the engine game state will update.
        Possible commands are:
        ========= ===============================================================
        command   Additional mandatory parameter
        --------- ---------------------------------------------------------------
        look
        move      <room>
        quit
        inspect   <item>
        use       <item>
        inventory
        hint
        save
        load
        :return: returns if the game should carry on running, if false,
        the quit has been called and the game will be ended.
        """
        self._transcript.append_log("User called " + command)
        match command.lower():
            case "quit":
                return self._do_quit()
            case "look":
                self._do_look()
            case move if move.startswith("move"):
                self._do_move(move)
            case inspect if inspect.startswith("inspect"):
                self._do_inspect(inspect)
            case use if use.startswith("use"):
                self._do_use()
            case "inventory":
                self._do_inventory()
            case "hint":
                self._do_hint()
            case "save":
                self._do_save()
            case "load":
                self._do_load()
            case _:
                self._transcript.print_message(
                    "Unknown command: " + str(command)
                    + ", type hint to see a list of available commands")
        return True

    def _do_quit(self) -> bool:
        self._transcript.print_message("Thank you for playing")
        self._transcript.save_transcript()
        return False

    def _do_inspect(self, inspect):
        """
        If you are in a valid location and inspect the right item,
        this will attempt to solve the room
        Relies on the current_room set in the engine
        :param inspect: The item to inspect
        :return: Nothing
        """
        is_valid = False
        commands = inspect.split(" ")
        if commands[0] == "inspect" and len(commands) > 1:
            item = commands[1]
            if item == CurrentRoom.get_room_item(self._current_location).value:
                is_valid = True
        if is_valid:
            try:
                match self._current_location:
                    case CurrentRoom.SOC:
                        from escaperoom.rooms.soc import SocRoom
                        soc_room = SocRoom(self._transcript)
                        self._inventory.update_inventory(
                            CurrentRoom.get_room_item(self._current_location),
                                                         soc_room.solve())
                    case CurrentRoom.DNS:
                        from escaperoom.rooms.dns import DNSRoom
                        dns_room = DNSRoom(self._transcript)
                        self._inventory.update_inventory(
                            CurrentRoom.get_room_item(self._current_location),
                                                         dns_room.solve())
                    case CurrentRoom.MALWARE:
                        from escaperoom.rooms.malware import MalwareRoom
                        malware_room = MalwareRoom(self._transcript)
                        self._inventory.update_inventory(
                            CurrentRoom.get_room_item(self._current_location),
                                                         malware_room.solve())
                    case CurrentRoom.VAULT:
                        from escaperoom.rooms.vault import VaultRoom
                        vault_room = VaultRoom(self._transcript)
                        self._inventory.update_inventory(
                            CurrentRoom.get_room_item(self._current_location),
                                                         vault_room.solve())
            except Exception as e:
                self._transcript.print_message("An error occurred in "
                                               "solving the room:")
                self._transcript.print_message(e)
        else:
            message = ("Please enter an item with the inspect command, "
                       "you are in ") + CurrentRoom.get_room_name(
                self._current_location)
            item_from_room = CurrentRoom.get_room_item(self._current_location)
            if item_from_room == Item.ITEM_NOTHING:
                message += " and there is nothing here"
            else:
                message += " and can inspect " + str(item_from_room.value)
            self._transcript.print_message(message)

    def _do_move(self, move):
        """
        Allows the user to move to a room specified, if the room is
        invalid also reports on it
        :param move:
        :return:
        """
        is_valid = False
        commands = move.split(" ")
        if commands[0] == "move" and len(commands) > 1:
            new_room = commands[1]
            match new_room.lower():
                case "dns":
                    self._current_location = CurrentRoom.DNS
                    is_valid = True
                case "malware":
                    self._current_location = CurrentRoom.MALWARE
                    is_valid = True
                case "soc":
                    self._current_location = CurrentRoom.SOC
                    is_valid = True
                case "vault":
                    self._current_location = CurrentRoom.VAULT
                    is_valid = True
                case "gate":
                    self._current_location = CurrentRoom.FINAL_GATE
                    is_valid = True
                case "lobby":
                    self._current_location = CurrentRoom.BASE
                    is_valid = True
        if not is_valid:
            self._transcript.print_message(
                "Please enter a room with the move command, possible rooms "
                "are dns, malware, soc, vault, gate, "
                "and lobby E.g. move dns")
        else:
            self._transcript.print_message(f"You have entered into "
                                           f"{self._current_location}")

    def _do_look(self):
        """
        Prints details about the current room the user is in
        :return: Nothing
        """
        match self._current_location:
            case CurrentRoom.BASE:
                self._transcript.print_message(
                    "You are in the lobby, "
                    "you can move to any room from here. "
                    "Where would you like to go?")
            case CurrentRoom.SOC:
                self._transcript.print_message(
                    "You are in the SOC room, there is a triage desk with a "
                    "large file of SSH logs, called auth.log, "
                    "that show authentication attempts. Your task is to "
                    "identify the most likely attacking subnet.")
            case CurrentRoom.MALWARE:
                self._transcript.print_message(
                    "You are in the Malware lab, there is a JSON-line file, "
                    "called proc_tree.jsonl, "
                    "that shows a process "
                    "tree containing a malicious chain ending with "
                    "an exfil command.")
            case CurrentRoom.VAULT:
                self._transcript.print_message(
                    "You are in the Vault, there is a text dump lying "
                    "on the table. Inside, there should be a valid "
                    "SAFE{a-b-c} code which satisfies a+b=c. Can you find it?")
            case CurrentRoom.DNS:
                self._transcript.print_message(
                    "You are in the DNS room, inside is a config file "
                    "which stores items as a key value pair. "
                    "Can you find the token_tag with the hintX value "
                    "to get the correct key value pair?")
            case CurrentRoom.FINAL_GATE:
                self._transcript.print_message(
                    "The final gate stands before you, have you collected "
                    "all the pieces to exit the gate?")

    def _do_use(self):
        """
        This function will use an item in the room, in the current specs
        this is only for using the gate
        :return: Nothing
        """
        if self._inventory.is_inventory_complete():
            with Transcript.open_file("final_gate.txt",
                                      "data") as final_gate_file:
                self._do_final_gate_file(final_gate_file)
        else:
            self._transcript.print_message("You do not have all the items, "
                                           "you are missing:")
            self._inventory.print_missing_items()

    def _do_inventory(self):
        """
        Prints a list of items you have in your inventory, these are tokens
        you have got for solving rooms
        :return: Nothing
        """
        self._transcript.print_message("You currently have the following "
                                       "items in your inventory:")
        self._inventory.print_inventory()

    def _do_hint(self):
        """
        Prints a list of commands the user can currently do
        :return: Nothing
        """
        self._transcript.print_message("look: Allows you to look in the "
                                       "current room and see what is "
                                       "available")
        self._transcript.print_message(
            "move <room>: Allows you to move to a room to solve, rooms "
            "available are: dns, malware, soc, vault, "
            "gate, and lobby")
        self._transcript.print_message(
            "inspect <item>: Allows you to inspect an item in the room. "
            "You are currently in "
            + CurrentRoom.get_room_name(self._current_location)
            + " and can inspect "
            + CurrentRoom.get_room_item(self._current_location).value)
        self._transcript.print_message(
            "use <item>: Depending on the room you are in, you can use "
            "an item to do an action. You are currently in "
            + CurrentRoom.get_room_name(self._current_location)
            + " and can use "
            + CurrentRoom.get_use_item(self._current_location))
        self._transcript.print_message("inventory: Prints a list of all items "
                                       "found your inventory")
        self._transcript.print_message(
            "save: Saves the progress of your current game to a file in the "
            "data folder, called save.json")
        self._transcript.print_message(
            "load: If a save.json file is found, in the data folder and it "
            "is valid,"
            "the system will load it and set that as your current progress. "
            "Will overwrite any progress already done in this session")
        self._transcript.print_message(
            "quit: Exits the game and prints currently collected evidence to "
            "a transcript file")
        self._transcript.print_message("hint: Gives a list of available "
                                       "commands")

    def _do_final_gate_file(self, final_gate_file):
        group_id_pattern = re.compile(r"\s*group_id\s*=\s*([\w-]*)")
        expected_hmac_pattern = re.compile(r"\s*expected_hmac\s*=\s*(\w*)")
        token_order_pattern = re.compile(
            r"\s*token_order\s*=\s*(\w*),(\w*),(\w*),(\w*)")
        final_gate_data = final_gate_file.read()
        group_id_tuple = group_id_pattern.findall(final_gate_data)
        expected_hmac_tuple = expected_hmac_pattern.findall(final_gate_data)
        token_order_tuple = token_order_pattern.findall(final_gate_data)
        if group_id_tuple is None or len(group_id_tuple) != 0:
            self._transcript.print_message("Group ID is in an invalid format")
        elif expected_hmac_tuple is None or len(expected_hmac_tuple) != 0:
            self._transcript.print_message(
                "Expected HMAC is in an invalid format")
        elif token_order_tuple is None or len(token_order_tuple) != 4:
            self._transcript.print_message(
                "Token order is in an invalid format")
        else:
            token_text = ""
            for token in token_order_tuple:
                if len(token_text) != 0:
                    token_text += "-"
                match token:
                    case "PID":
                        token_text += self._inventory.inventory[
                            Item.ITEM_MALWARE]
                    case "DNS":
                        token_text += self._inventory.inventory[Item.ITEM_DNS]
                    case "KEYPAD":
                        token_text += self._inventory.inventory[Item.ITEM_SOC]
                    case "SAFE":
                        token_text += self._inventory.inventory[
                            Item.ITEM_VAULT]
                    case _:
                        self._transcript.print_message(
                            f"Invalid token of type {token}")
                        return
            final_gate_text = (
                f"FINAL_GATE=PENDING\nMSG={group_id_tuple[0]}|{token_text}\n"
                f"EXPECTED_HMAC={expected_hmac_tuple[0]}")
            self._transcript.transcript_dict[
                CurrentRoom.FINAL_GATE] = final_gate_text
            self._do_quit()

    def _do_save(self):
        """
        Saves the current state of the game
        :return: Nothing
        """
        if self._utils.save():
            self._transcript.print_message("You saved the current game "
                                           "successfully")
        else:
            self._transcript.print_message("You did not save the current "
                                           "game successfully")

    def _do_load(self):
        """
        Loads the current state of the game from a save.txt file
        :return: Nothing
        """
        if self._utils.load():
            self._transcript.print_message("You loaded the current game "
                                           "successfully")
        else:
            self._transcript.print_message("You did not load the current "
                                           "game successfully")
