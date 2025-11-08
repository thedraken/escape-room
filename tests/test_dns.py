"""
Test class for dns.py, runs the methods and makes sure they behave as
expected.
"""
import io

from escaperoom.location import CurrentRoom
from escaperoom.rooms.dns import DNSRoom
from escaperoom.transcript import Transcript


def _room_log(t: Transcript, room: CurrentRoom) -> str:
    """
    Helper: return all text that was logged to the transcript for a specific room
    The transcript internally keeps logs per room, so using this for assertions
    """
    return t.transcript_dict[room]


def test_dns_happy_path_token_phrase():
    """
    Test: DNSRoom correctly decodes the right hint when token_tag = 'NA==' → '4' → hint4.
    The decoded text for hint4 ends with 'phrase.', so the token should be 'phrase'.
    """
    # fake dns.cfg contents, messy, with duplicates, base64 strings, and comments
    cfg = """# DNS zone fragment with TXT-like hints
env = lab-segment
hint1 = SWdub3JlIHRoaXMg\\
        aGludCBwbGVhc2U=
hint1 = SWdub3JlIHRoaXMg\\
        aGludCBwbGVhc2U=
hint5 = R29vZ2xlIGlzIG5vdCBhIHRva2VuLg=
        hint6 = QmFkIGJhc2U2NCB5b3UgZm91bmQ/
hint6 = QmFkIGJhc2U2NCB5b3UgZm91bmQ/
hint3 = QmFkIGJhc2U2NCB5b3UgZm91bmQ_
        hint2 = SWdub3JlIHRoaXMgaGludCBwbGVhc2U=
        hint4  =  TG9vayBpbnNpZGUgdGhlIEROUyBzd2l0Y2ggZm9yIHRoZSByaWdodCBwaHJhc2Uu
token_tag = NA==
note = this_is_not_base64
# end
"""

    # Transcript needs a folder path (uses "data" for it)
    t = Transcript("data")

    # Create a DNSRoom instance for testing, the save path is irrelevant here
    room = DNSRoom(t, save_file_path="ignored")

    # Replace open_file() so it reads from fake config instead of disk
    room.open_file = lambda: io.StringIO(cfg)

    # Run the actual solver logic
    token = room.solve()

    # The token extracted from the last word of hint4’s decoded line
    assert token == "phrase"

    # Retrieve what the solver wrote into the transcript log
    log = _room_log(t, CurrentRoom.DNS)

    # Check that the grader-required lines are logged correctly
    assert "TOKEN[DNS]=phrase" in log
    assert "EVIDENCE[DNS].KEY=hint4" in log
    assert "Look inside the DNS switch for the right phrase." in log


def test_dns_handles_bad_hints_but_uses_correct_one():
    """
    Even if other hints are broken base64, DNSRoom should still decode the one named by token_tag.
    """
    cfg = """
hint1 = !!!not_base64!!!
hint4 = TG9vayBpbnNpZGUgdGhlIEROUyBzd2l0Y2ggZm9yIHRoZSByaWdodCBwaHJhc2Uu
token_tag = hint4
"""

    #mock transcript + room setup
    t = Transcript("data")
    room = DNSRoom(t, save_file_path="ignored")

    # Fake file input with StringIO
    room.open_file = lambda: io.StringIO(cfg)

    # Run solve, it should ignore bad hints and use hint4
    token = room.solve()
    assert token == "phrase"
