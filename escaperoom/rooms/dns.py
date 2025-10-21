"""
DNSRoom - solves the DNS Closet puzzle.
Reads a messy config file (dns.cfg) with base64-encoded hints,
finds which hint to decode based on token_tag, and extracts
the last word of that decoded hint as the token.
"""

import base64
import re
from typing import Dict, Optional, Tuple

from escaperoom.location import CurrentRoom
from escaperoom.rooms.base import BaseRoom
from escaperoom.transcript import Transcript


class DNSRoom(BaseRoom):
    """
    DNS puzzle logic:
    - Reads key=value pairs from data/dns.cfg (ignores # comments and blanks)
    - Base64-decodes hints like hint1..hintN
    - token_tag can be plain or base64 (e.g. 'NA==' -> '4')
    - Token = last word in decoded hint sentence
    - Logs:
        TOKEN[DNS]=<token>
        EVIDENCE[DNS].KEY=<hintX>
        EVIDENCE[DNS].DECODED_LINE=<decoded sentence>
    """

    def __init__(self, transcript: Transcript):
        super().__init__(transcript, CurrentRoom.DNS)

    def _parse_kv_line(self, line: str) -> Optional[Tuple[str, str]]:
        """
        Parse 'key=value' ignoring comments, blank lines, and weird spacing.
        Returns (key, value) or None if invalid.
        """
        no_comment = line.split("#", 1)[0].strip()
        if not no_comment or "=" not in no_comment:
            return None
        k, v = no_comment.split("=", 1)
        return k.strip(), v.strip()

    def _b64_decode_loose(self, s: str) -> Optional[str]:
        """
        Base64-decode tolerant of bad padding and whitespace.
        Returns decoded string or None if decoding fails.
        """
        compact = re.sub(r"\s+", "", s)
        compact += "=" * ((4 - len(compact) % 4) % 4)
        try:
            return base64.b64decode(compact, validate=False).decode("utf-8", errors="replace")
        except Exception:
            return None

    def _last_word(self, s: str) -> str:
        """
        Extract the last alphanumeric word from string s.
        Returns empty string if none found.
        """
        words = re.findall(r"[A-Za-z0-9_]+", s)
        return words[-1] if words else ""

    def solve(self):
        """
        Main solver for the DNS room.
        Called when user runs `inspect dns.cfg` in the game.
        """
        self.transcript.print_message("You called solve on " +
                                      CurrentRoom.get_room_name(
                                          self.current_room))
        self.transcript.print_message("[DNSRoom] starting decode")

        try:
            cfg = self.open_file()
            if cfg is None:
                self.transcript.print_message("dns.cfg not found in data/.")
                return None

            # Step 1: parse the config file
            raw: Dict[str, str] = {}
            with cfg:
                for raw_line in cfg:
                    parsed = self._parse_kv_line(raw_line)
                    if parsed:
                        k, v = parsed
                        raw[k] = v  # latest key wins (handles duplicates)

            if not raw:
                self.transcript.print_message(
                    "dns.cfg contained no usable entries.")
                return None

            # Step 2: decode all hintN values
            decoded_hints: Dict[str, str] = {}
            for k, v in raw.items():
                if re.fullmatch(r"hint\d+", k, flags=re.IGNORECASE):
                    dec = self._b64_decode_loose(v)
                    if dec:
                        decoded_hints[k] = dec

            # Step 3: get token_tag (may be base64-encoded)
            token_key_raw = raw.get("token_tag") or raw.get("tokenTag") or raw.get("token")
            if not token_key_raw:
                self.transcript.print_message(
                    "token_tag not found in dns.cfg.")
                return None

            token_key_raw = token_key_raw.strip()
            decoded_token_tag = self._b64_decode_loose(token_key_raw)
            token_key = decoded_token_tag.strip() if decoded_token_tag else token_key_raw

            if not re.fullmatch(r"hint\d+", token_key, flags=re.IGNORECASE):
                self.transcript.print_message(
                    f"token_tag invalid or not a hint key: {token_key}")
                return None

            # Step 4: decode the indicated hint
            decoded_sentence = decoded_hints.get(token_key)
            if not decoded_sentence:
                self.transcript.print_message(
                    f"Could not decode value for {token_key}.")
                return None

            # Step 5: extract the token
            token = self._last_word(decoded_sentence)
            if not token:
                self.transcript.print_message(
                    f"No valid last word in decoded line for {token_key}.")
                return None

            # Step 6: log everything and print confirmation
            self.transcript.print_message("[Room DNS] Decoding hints...")
            self.transcript.print_message(
                f"Decoded line: \"{decoded_sentence}\"")
            self.transcript.print_message(f"Token formed: {token}")

            self.add_log_to_transcript(f"TOKEN[DNS]={token}\n")
            self.add_log_to_transcript(f"EVIDENCE[DNS].KEY={token_key}\n")
            self.add_log_to_transcript(f"EVIDENCE[DNS].DECODED_LINE"
                                       f"={decoded_sentence}\n")

            return token

        except Exception as e:
            self.transcript.print_message(f"Error in DNSRoom: {e}")
            return None