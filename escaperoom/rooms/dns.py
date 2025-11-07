"""
DNSRoom

This class solves the DNS puzzle by:
- Reading a messy `data/dns.cfg` file (key=value pairs).
- Ignoring comments, blank lines, weird spacing, and duplicate keys (last wins).
- Decoding Base64-encoded hints named hint1, hint2, ...
- Using `token_tag` (which may itself be Base64) to decide which hint to use.
- Extracting the last word of that decoded hint as the token.

Transcript (grader) lines we must write:
    TOKEN[DNS]=<token>
    EVIDENCE[DNS].KEY=<hintX>
    EVIDENCE[DNS].DECODED_LINE=<decoded sentence>
"""

import base64
import binascii
import codecs
import re
from typing import Dict, Optional, Tuple

from escaperoom.location import CurrentRoom
from escaperoom.rooms.base import BaseRoom
from escaperoom.transcript import Transcript


class DNSRoom(BaseRoom):
    """
    DNS room solver.

    Robustness highlights:
    - Safe parsing: comments stripped, blanks ignored, '=' inside values allowed
    - Duplicate keys: later entries overwrite earlier ones ( config behavior)
    - Base64 decode is whitespace-tolerant and auto-pads '=' to avoid decode crashes
    - `token_tag` may be Base64 (e.g., "NA==" → "4" → we interpret as "hint4")
    - Token = last alphanumeric/underscore word in the decoded hint sentence
    """

    def __init__(self, transcript: Transcript, save_file_path: str):
        """
        ctor

        Args:
            transcript: Shared transcript/logger object used by the engine.
            save_file_path: project’s BaseRoom expects a save path; pass it through

        Side effects:
            - Calls BaseRoom ctor with (transcript, CurrentRoom.DNS, save_file_path)
        """
        super().__init__(transcript, CurrentRoom.DNS, save_file_path)

    # Helper methods

    @staticmethod
    def _parse_kv_line(line: str) -> Optional[Tuple[str, str]]:
        """
        Parse ONE config line into a (key, value) tuple, or return None if junk

        Why this exists:
        - The config is intentionally messy: comments at the end of lines (# ...),
          extra whitespace, sometimes lines without '=', and sometimes duplicate keys
        - only want "key = value" pairs, ignoring everything else.

        Parsing strategy:
        1) Remove trailing inline comments (split at '#', take the left side)
        2) Trim whitespace
        3) If the remaining text has no '=', ignore it
        4) Split on the FIRST '=' only (values might contain '=' later)
        5) Strip spaces around key and value
        6) If key is empty ( '= value'), ignore the line.

        Returns:
            (key, value) on success, otherwise None
        """
        # Remove trailing comment and leading/trailing spaces
        no_comment = line.split("#", 1)[0].strip()
        if not no_comment or "=" not in no_comment:
            return None  # blank line or no key=value present

        # Only split on the FIRST '=' so values can still include '='
        key, value = no_comment.split("=", 1)
        key, value = key.strip(), value.strip()
        if not key:  # invalid if key ended up empty ( "= value")
            return None
        return key, value

    def _b64_decode_loose(self, s: str, convert_to_rot_if_fail: bool) -> Optional[str]:
        """
        Tolerant Base64 decode.

        Why "loose"?
        - The file can include whitespace/newlines/backslash continuations inside the encoded value
        - Some entries may be missing '=' padding; we add it so length % 4 == 0
        - We decode to UTF-8 and replace any weird bytes instead of crashing
        
        :param s: The base64 text to decode.
        :param convert_to_rot_if_fail: If the initial convertion fails due
        to missing spaces and this is set to true, will run a rot13
        convertion on the base64 text before decoding.

        :returns: Decoded string on success, or None if decoding fails

        Notes:
            match specific decode errors (ValueError, binascii.Error) so pylint
            doesn’t flag a broad exception here
        """
        try:
            # Strip ALL whitespace (spaces, tabs, newlines, accidental splits).
            compact = re.sub(r"\s+", "", s)

            # Base64 requires length to be a multiple of 4; add '=' padding if needed
            compact += "=" * ((4 - len(compact) % 4) % 4)
            # validate=False -> accept non canonical alphabets/padding quietly
            decoded_bytes = base64.b64decode(compact, validate=False)
            return_value = decoded_bytes.decode("utf-8", errors="replace")
            if not convert_to_rot_if_fail and " " not in return_value:
                return self._b64_decode_loose(codecs.decode(s, "rot13"), True)
            return return_value
        except (ValueError, binascii.Error) as err:
            # some hints are intentionally bad/noise
            self.transcript.print_message(f"Base64 decode error: {err}")
            return None

    @staticmethod
    def _last_word(s: str) -> str:
        """
        Extract the LAST 'word' from the string.
        Definition of 'word' here:
        - One or more of letters/digits/underscore (no punctuation)
        Example
          "Look at the right phrase." -> "phrase"
        Returns:
            The last word, or "" if none found
        """
        words = re.findall(r"[A-Za-z0-9_]+", s)
        return words[-1] if words else ""

    # Main solver

    def solve(self) -> Optional[str]:
        """
        Entry point when the player runs `inspect dns.cfg`.

        High-level steps:
          1) Read and parse the config into a dict; later duplicates overwrite earlier ones
          2) Base64-decode all hintN entries into `decoded_hints`
          3) Determine the right hint via `token_tag` (may itself be Base64)
             - If token_tag decodes to digits (e.g., "4"), we turn it into "hint4"
          4) Look up the decoded sentence for that hint and extract the token (last word)
          5) Print progress for the player and write grading lines via Transcript

        Returns:
            The token string if successful, otherwise None.
        """
        # Clear, user-facing trace so the player knows what’s happening
        self.transcript.print_message("[DNSRoom] starting decode")

        try:
            # BaseRoom.open_file() uses CurrentRoom.get_room_item(self.current_room).value
            # DNS -> "dns.cfg",  Returns an open file handle or None
            fh = self.open_file()
            if fh is None:
                self.transcript.print_message("dns.cfg not found in data/.")
            else:
                # Build dict of key/value pairs from the file
                # NOTE: If a key appears multiple times, the *last* value wins!!!
                raw: Dict[str, str] = {}
                with fh:
                    for line in fh:
                        parsed = self._parse_kv_line(line)
                        if parsed:
                            key, value = parsed
                            raw[key] = value  # overwrite earlier duplicates by design

                if not raw:
                    self.transcript.print_message("dns.cfg contained no valid entries.")
                    return None

                decoded_hints = self.decode_hints(raw)

                # Determine which hint to use via token_tag
                # naming in case the file uses tokenTag or token
                token_tag_raw = raw.get("token_tag") or raw.get("tokenTag") or raw.get("token")
                if not token_tag_raw:
                    self.transcript.print_message("token_tag not found in dns.cfg.")
                    return None

                token_tag_raw = token_tag_raw.strip()

                # Try to Base64-decode token_tag itself, example: NA== -> 4
                token_key = (self._b64_decode_loose(token_tag_raw, True
                                                    ) or token_tag_raw).strip()

                # If token_key is just digits, we interpret it as "hint<digits>"
                # e.g., "4" -> "hint4"
                if token_key.isdigit():
                    token_key = f"hint{token_key}"

                # Validate that we ended up with something like "hint4"
                if not re.fullmatch(r"hint\d+", token_key, flags=re.IGNORECASE):
                    self.transcript.print_message(f"token_tag invalid or "
                                                  f"not a hint key: {token_key}")
                    return None

                # Get the decoded sentence and extract the token
                decoded_sentence = decoded_hints.get(token_key)
                if not decoded_sentence:
                    # Either the hint key didn't exist or it couldn't be decoded.
                    self.transcript.print_message(f"Could not decode the value for {token_key}.")
                    return None

                token = self._last_word(decoded_sentence)
                if token:
                    # messages are for the console
                    self.transcript.print_message("[Room DNS] Decoding hints...")
                    self.transcript.print_message(f'Decoded line: "{decoded_sentence}"')
                    self.transcript.print_message(f"Token formed: {token}")

                    # lines are expected in run.txt
                    self.add_log_to_transcript(f"TOKEN[DNS]={token}")
                    self.add_log_to_transcript(f"EVIDENCE[DNS].KEY={token_key}")
                    self.add_log_to_transcript(f"EVIDENCE[DNS].DECODED_LINE={decoded_sentence}")

                    return token
                self.transcript.print_message(
                    f"No valid last word found in decoded line for {token_key}."
                )
        except FileNotFoundError:
            # defensive: open_file() normally returns None if missing (handles direct errors too)
            self.transcript.print_message("dns.cfg not found (FileNotFoundError).")
        except Exception as err:  # pylint: disable=broad-exception-caught
            # error to the transcript, keep the engine alive
            self.transcript.print_message(f"Error in DNSRoom: {err}")
        return None

    def decode_hints(self, raw: dict[str, str]) -> dict[str, str]:
        """
        Will take the items and try to find the hint and decode them
        :param raw: raw data
        :return: decoded hints
        """
        # Base64-decode all hintN values
        # only attempt to decode keys named 'hint<digits>'
        decoded_hints: Dict[str, str] = {}
        for key, val in raw.items():
            if re.fullmatch(r"hint\d+", key, flags=re.IGNORECASE):
                decoded = self._b64_decode_loose(val, False)
                if decoded:
                    decoded_hints[key] = decoded
                # If a hint fails to decode, we just skip it ( some are intentional noise)
        return decoded_hints
