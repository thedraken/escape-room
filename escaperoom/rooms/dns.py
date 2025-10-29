"""
DNSRoom 

WHAT THIS CLASS DOES:
- Reads `data/dns.cfg` which is a messy "key = value" config file.
- Lines may have extra spaces, comments (# ...), accidental line breaks, and duplicate keys.
- Keys named `hint1`, `hint2`, ... contain Base64-encoded sentences.
- The line `token_tag = <...>` tells us WHICH hint to use. Trick: <...> can itself be Base64,
  e.g., "NA==" -> "4" -> so we actually want hint4.
- The TOKEN we need to submit is the **last word** of the decoded sentence for that hint.
- We must also write grading lines to run.txt via Transcript:
      TOKEN[DNS]=<token>
      EVIDENCE[DNS].KEY=<hintX>
      EVIDENCE[DNS].DECODED_LINE=<the full decoded sentence>
"""

import base64
import re
from typing import Dict, Optional, Tuple

# project’s structure uses escaperoom.location
from escaperoom.location import CurrentRoom
from escaperoom.rooms.base import BaseRoom
from escaperoom.transcript import Transcript


class DNSRoom(BaseRoom):
    """
    Implements the DNS room solver

    Major robustness features:
    - Ignores comments and blank lines
    - Accepts "key = value" with arbitrary spacing; supports '=' inside the value
    - Handles duplicate keys: the last one wins
    - Tolerant Base64 decoding:
        * strips whitespace/newlines
        * auto-adds '=' padding to a multiple of 4
        * doesn't crash if decoding fails (returns None)
    - token_tag may itself be Base64 (e.g., "NA==" -> "4");
    if it's a digit after decoding, we turn it into "hint4".
    - Token is the last alphanumeric word in the decoded sentence.
    """

    def __init__(self, transcript: Transcript):
        # BaseRoom stores the transcript and which room this is
        super().__init__(transcript, CurrentRoom.DNS)

    # helper functions

    @staticmethod
    def _parse_kv_line(line: str) -> Optional[Tuple[str, str]]:
        """
        Parse one config line into (key, value), or return None if the line is junk

        Rules:
        - Strip off anything after a '#' (comment)
        - Ignore blank lines
        - Require at least one '='; split only on the FIRST '=', so values can contain '='
        - Trim spaces around key and value
        """
        # removes trailing inline comment and surrounding spaces
        no_comment = line.split("#", 1)[0].strip()
        if not no_comment or "=" not in no_comment:
            return None  # empty, comment-only, or invalid line

        key, value = no_comment.split("=", 1)  # split on FIRST '=' only
        key = key.strip()
        value = value.strip()
        if not key:  # invalid if there’s no key
            return None
        return key, value

    def _b64_decode_loose(self, s: str) -> Optional[str]:
        """
        Base64-decode, but be forg:
        - Removes all whitespace (line wraps/backslashes in cfg)
        - Adds '=' padding so length is a multiple of 4
        - Returns decoded text as UTF-8 (replacing bad bytes), or None if decode fails completely
        """
        try:
            # Remove all whitespace (spaces, tabs, newlines, backslash-newline artifacts)
            compact = re.sub(r"\s+", "", s)
            # Add padding if needed to make len % 4 == 0
            compact += "=" * ((4 - len(compact) % 4) % 4)
            decoded_bytes = base64.b64decode(compact, validate=False)
            return decoded_bytes.decode("utf-8", errors="replace")
        except Exception as e:  # pylint: disable=broad-except
            self.transcript.print_message(f"Error decoding data {e}")
            return None  # if truly undecodable, treat as absent

    @staticmethod
    def _last_word(s: str) -> str:
        """
        Return the LAST "word" in s, where a word = letters/digits/underscore.
        Punctuation and spaces are ignored. If nothing matches, return ""
        """
        words = re.findall(r"[A-Za-z0-9_]+", s)
        return words[-1] if words else ""

    #  main solver

    def solve(self) -> Optional[str]:
        """
        Top-level entry point called by the engine when the player does `inspect dns.cfg`

        Steps:
          1) Open data/dns.cfg; parse into a dict (later duplicates overwrite earlier ones)
          2) Base64-decode every key that looks like "hint<digits>"
          3) Read token_tag. If token_tag itself looks base64 (e.g., "NA=="), decode it first
             - If the decoded token_tag is a pure number (e.g., "4"), transform to "hint4"
          4) Pull the decoded sentence for that hint and extract the last word as the token
          5) Print user feedback and write the official grading lines to run.txt via Transcript
        """
        #console markers so the player sees what’s happening.
        self.transcript.print_message("[DNSRoom] starting decode")

        try:
            # BaseRoom.open_file() uses CurrentRoom.get_room_item(self.current_room).value
            # which for DNS -> "dns.cfg". It returns an open file handle or None.
            fh = self.open_file()
            if fh is None:
                self.transcript.print_message("dns.cfg not found in data/.")
                return None

            # 1) parse entire file into a dict `raw` (last key wins)
            raw: Dict[str, str] = {}
            with fh:
                for raw_line in fh:
                    parsed = self._parse_kv_line(raw_line)
                    if parsed is None:
                        continue
                    k, v = parsed
                    raw[k] = v  # overwrite duplicates by design (latest occurrence wins)

            if not raw:
                self.transcript.print_message("dns.cfg contained no valid key=value lines.")
                return None

            # 2) decode all hintN values into `decoded_hints`
            decoded_hints: Dict[str, str] = {}
            for k, v in raw.items():
                # Only decode keys that match hint + digits
                if re.fullmatch(r"hint\d+", k, flags=re.IGNORECASE):
                    decoded = self._b64_decode_loose(v)
                    if decoded:
                        decoded_hints[k] = decoded
                    # If decoding fails, simply don't include it, that's intentional:
                    # some hints are not good by design.

            # 3)figuring out which hint to use via token_tag
            # token_tag may appear under a little different names
            token_tag_raw = raw.get("token_tag") or raw.get("tokenTag") or raw.get("token")
            if not token_tag_raw:
                self.transcript.print_message("token_tag not found in dns.cfg.")
                return None

            token_tag_raw = token_tag_raw.strip()

            # Try to base64-decode token_tag in case it's like "NA==" (which: "4")
            decoded_tag = self._b64_decode_loose(token_tag_raw)
            token_key = decoded_tag.strip() if decoded_tag else token_tag_raw

            # If token_key is purely digits, it means "use hint<digits>"
            # example: "4" -> "hint4"
            if token_key.isdigit():
                token_key = f"hint{token_key}"

            # here validates final token_key format
            if not re.fullmatch(r"hint\d+", token_key, flags=re.IGNORECASE):
                self.transcript.print_message(f"token_tag invalid or not a hint key: {token_key}")
                return None

            #  4) get decoded sentence for chosen hint and extract token
            decoded_sentence = decoded_hints.get(token_key)
            if not decoded_sentence:
                # Either the hint line didn't exist or couldn't be decoded
                self.transcript.print_message(f"Could not decode the value "
                                              f"for {token_key}.")
                return None

            token = self._last_word(decoded_sentence)
            if not token:
                self.transcript.print_message(f"No valid last word found in "
                                              f"decoded line for {token_key}.")
                return None

            # 5) user feedback &official grading logs
            self.transcript.print_message("[Room DNS] Decoding hints...")
            self.transcript.print_message(f'Decoded line: "{decoded_sentence}"')
            self.transcript.print_message(f"Token formed: {token}")

            # These lines get appended to run.txt when
            # Transcript.save_transcript() runs
            self.add_log_to_transcript(f"TOKEN[DNS]={token}")
            self.add_log_to_transcript(f"EVIDENCE[DNS].KEY={token_key}")
            self.add_log_to_transcript(f"EVIDENCE[DNS].DECODED_LINE={decoded_sentence}")

            return token

        except Exception as e:  # pylint: disable=broad-except
            # don't crash the engine; report the error to the transcript for debugging
            self.transcript.print_message(f"An error occurred in DNSRoom:\n{e}")
            return None
