"""
TODO Add comment about what file contains
"""
import base64
import re
from typing import Dict, Optional, Tuple

from escaperoom.location import CurrentRoom
from escaperoom.rooms.base import BaseRoom
from escaperoom.transcript import Transcript


class DNSRoom(BaseRoom):
    """
    DNS puzzle:
    - Read key=value pairs from data/dns.cfg (ignore blank lines and
    '#' comments).
    - Base64-decode values for keys like hint1, hint2, ... (robust to
    missing padding).
    - Use the key named by 'token_tag' (e.g., token_tag=hint2).
    - The token is the LAST WORD of that decoded hint sentence.
    - Log to run.txt:
        TOKEN[DNS]=<token>
        EVIDENCE[DNS].KEY=<hintX>
        EVIDENCE[DNS].DECODED_LINE=<full decoded sentence>
    """

    def __init__(self, transcript: Transcript):
        # Call parent constructor, telling BaseRoom which room this is
        # (CurrentRoom.DNS)
        super().__init__(transcript, CurrentRoom.DNS)

    # shows in console so you know this code is actually loaded
    def _marker(self):
        self.transcript.print_message("[DNSRoom v2] starting decode")

    @staticmethod
    def _parse_kv_line(line: str) -> Optional[Tuple[str, str]]:
        """
        Parse a single line into (key, value) or return None.
        - Strips comments starting with '#'
        - Ignores blank lines or lines without '='
        - Preserves value exactly after the first '=' (allowing '=' in values)
        """
        no_comment = line.split("#", 1)[0].strip()
        if not no_comment or "=" not in no_comment:
            return None
        key, value = no_comment.split("=", 1)
        key = key.strip()
        value = value.strip()
        if not key:
            return None
        return key, value

    def _b64_decode_loose(self, s: str) -> Optional[str]:
        """
        Try to base64-decode `s` tolerantly.
        - Removes whitespace (helps with accidentally line-broken base64)
        - Adds '=' padding to make length a multiple of 4
        - Uses errors='replace' on decode so invalid bytes won't crash
        - Returns decoded string or None on failure
        """
        compact = re.sub(r"\s+", "", s)  # remove spaces/newlines
        # inside the value
        pad_needed = (-len(compact)) % 4  # how many '=' to add (0..3)
        compact += "=" * pad_needed
        try:
            # permissive decode
            decoded = base64.b64decode(compact, validate=False)
            return decoded.decode("utf-8", errors="replace")
        except Exception as e:
            self.transcript.print_message("An error occurred:")
            self.transcript.print_message(e)
            return None

    @staticmethod
    def _last_word(s: str) -> str:
        """
        Extract the last 'word' from string s.
        - Word defined as run of letters/digits/underscore
        (so punctuation ignored).
        - Returns empty string if no word found.
        """
        words = re.findall(r"[A-Za-z0-9_]+", s)
        return words[-1] if words else ""

    def solve(self):
        """
        Main entry called by the engine when player does `inspect dns.cfg`.
        Steps:
         1. Ensure dns.cfg exists and open it.
         2. Parse every key=value into dict `raw`.
         3. Base64-decode all keys that match hintN into `decoded_hints`.
         4. Read token_tag (must be 'hintX') and find the corresponding
         decoded hint.
         5. Extract last word as token, print user messages, and write
         the required transcript lines.
        """
        # entry message 
        self.transcript.print_message("You called solve on "
                                      + CurrentRoom.get_room_name(
            self.current_room))
        self._marker()

        try:
            cfg = self.open_file()  # BaseRoom.open_file opens data/dns.cfg
            # if present
            if cfg is None:
                self.transcript.print_message("dns.cfg not found in data/.")
                return None

            # 1) Parse the file into a dictionary of raw key->value
            raw: Dict[str, str] = {}
            with cfg:
                for raw_line in cfg:
                    parsed = self._parse_kv_line(raw_line)
                    if parsed is None:
                        continue
                    k, v = parsed
                    raw[k] = v  # latest occurrence wins for duplicate keys

            if not raw:
                self.transcript.print_message("dns.cfg contained no usable "
                                               "key=value entries.")
                return None

            # 2) Decode hintN values
            decoded_hints: Dict[str, str] = {}
            for k, v in raw.items():
                if re.fullmatch(r"hint\d+", k, flags=re.IGNORECASE):
                    dec = self._b64_decode_loose(v)
                    if dec is not None:
                        decoded_hints[k] = dec

            # 3) Find token_tag entry (several common names allowed)
            token_key = (raw.get("token_tag") or raw.get("tokenTag")
                         or raw.get("token"))
            if not token_key:
                self.transcript.print_message("token_tag not found in "
                                               "dns.cfg.")
                return None

            token_key = token_key.strip()
            # token_tag must literally name the hint key (example 'hint2')
            if not re.fullmatch(r"hint\d+", token_key,
                                flags=re.IGNORECASE):
                self.transcript.print_message(f"token_tag points to an "
                                               f"invalid key: {token_key}")
                return None

            # get the decoded sentence for the indicated hint
            decoded_sentence = decoded_hints.get(token_key)
            if not decoded_sentence:
                # either the hint didn't exist or could not be decoded
                self.transcript.print_message(f"Could not decode the value "
                                               f"for {token_key} as base64.")
                return None

            # 4) Extract token as last word and validate
            token = self._last_word(decoded_sentence)
            if not token:
                self.transcript.print_message(f"Decoded sentence for "
                                               f"{token_key} "
                                               f"had no valid last word.")
                return None

            # 5) Print user-facing messages and append the official
            # grading logs
            self.transcript.print_message("[Room DNS] Decoding hints...")
            self.transcript.print_message(f"Decoded line: "
                                           f"\"{decoded_sentence}\"")
            self.transcript.print_message(f"Token formed: {token}")

            # The lines below are what will be written to data/run.txt
            # by Transcript.save_transcript()
            self.add_log_to_transcript(f"TOKEN[DNS]={token}\n")
            self.add_log_to_transcript(f"EVIDENCE[DNS].KEY={token_key}\n")
            self.add_log_to_transcript(f"EVIDENCE[DNS].DECODED_LINE="
                                        f"{decoded_sentence}\n")
            return token

        except FileNotFoundError:
            # defensive: open_file should return None, but handle file
            # errors gracefully
            self.transcript.print_message("dns.cfg not found "
                                           "(FileNotFoundError).")
            return None
        except Exception as e:
            # catch-all to avoid crashing the engine; report to transcript
            # for debugging
            self.transcript.print_message("An error occurred in DNSRoom:\n"
                                          + str(e))
            return None
