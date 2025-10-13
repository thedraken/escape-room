from enum import Enum


class CurrentRoom(Enum):
    BASE = 1
    SOC = 2
    DNS = 3
    VAULT = 4
    MALWARE = 5
    FINAL_GATE = 6

    @staticmethod
    def get_room_name(current_room: Enum):
        match current_room:
            case CurrentRoom.BASE:
                return "Lobby"
            case CurrentRoom.SOC:
                return "SOC"
            case CurrentRoom.DNS:
                return "DNS"
            case CurrentRoom.VAULT:
                return "Vault"
            case CurrentRoom.MALWARE:
                return "Malware"
            case CurrentRoom.FINAL_GATE:
                return "Final Gate"
        return None

    @staticmethod
    def get_room_item(current_room: Enum):
        match current_room:
            case CurrentRoom.DNS:
                return "dns.cfg"
            case CurrentRoom.VAULT:
                return "vault_dump.txt"
            case CurrentRoom.MALWARE:
                return "pro_tree.jsonl"
            case CurrentRoom.SOC:
                return "auth.log"
            case CurrentRoom.FINAL_GATE:
                return "final_gate.txt"
        return "no item"

    @staticmethod
    def get_use_item(current_room: Enum):
        match current_room:
            case CurrentRoom.FINAL_GATE:
                return "gate"
        return "nothing"
