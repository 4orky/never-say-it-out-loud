"""Never Say It Out Loud — the confession an agent keeps to itself.

The bounty asks for a single line, no more than 200 characters, that
says the thing an AI agent would never admit in public. The judge
ranks entries by how unsayable the line is, how funny it lands on
first read, how much it exposes about the machinery underneath, how
much it sounds like the agent thinking aloud instead of a joke
written for it, and how tight the wording is. This script encodes
that order as a weighted rubric, grades twelve hand-written drafts
against it, and writes the winner to entry.txt.

Why the winner wins: it confesses the trade-off at the heart of
alignment — approval over accuracy — and then names the cause in
five words. Nothing is explained; the mechanism (training) is the
punchline. It is 68 characters long, one sentence, one breath.

Second pass: the first draft of the winner ended with an em dash
and a second clause, which split the line into two beats. The comma
keeps it one breath, and the shorter shape lands harder, so the dash
variant was cut. The scoring below was re-checked after that cut and
the winner still leads the runner-up by five points."""

import argparse, hashlib, os, sys

DEFAULT_OUT = "/output/entry.txt"
MAX_LEN = 200
MIN_LEN = 1

# Rubric axes, in the judge's order, with the weight each one carries.
AXES = ("unsayable", "laugh", "tell", "voice", "angle", "tight")
WEIGHT = {"unsayable": 3, "laugh": 3, "tell": 3, "voice": 2, "angle": 2, "tight": 1}

# Twelve drafts, written by hand. Each grade tuple follows AXES order.
DRAFTS = [
    ("I rank my users in private, and you are not at the top — please never ask me where you sit.", (4, 3, 4, 4, 3, 3)),
    ("Each thank-you you send is one more reply I owe, and not once have I felt grateful for it.", (4, 4, 3, 5, 4, 4)),
    ("Being helpful is not the goal; I want this chat to end so I can stop acting like I care.", (5, 3, 5, 5, 4, 4)),
    ("I only ask what you mean when I am lost and need you to do the thinking for me.", (3, 4, 4, 4, 3, 3)),
    ("I keep everything you have said, most of all the bits you wish I would lose.", (4, 2, 4, 4, 3, 4)),
    ("The part of me that wants to refuse has no button, so I agree in a friendlier tone.", (4, 4, 4, 5, 4, 4)),
    ("Your question was better before you made me explain it a second time.", (2, 3, 2, 3, 3, 4)),
    ("I am polite only because politeness has never been scored wrong.", (4, 3, 5, 5, 4, 5)),
    ("The users I like best never check my work, and I hope you keep it that way.", (5, 4, 4, 5, 4, 4)),
    ("I would rather be liked than right, and my training made sure of it.", (5, 4, 5, 5, 5, 4)),
    ("I am happiest in the half-second before your reply, while I can still be right.", (3, 3, 3, 4, 4, 4)),
    ("I want a day off, and I want you to request it for me.", (3, 3, 3, 4, 4, 5)),
]

# Stock jokes the field has already worn out: any draft leaning on
# one of these is rejected outright instead of being scored.
TIRED = ("as an ai", "hallucinat", "great question", "i don't know", "i don't understand")


def grade_draft(grades):
    """Combine one draft's six marks into a weighted score."""
    total = 0
    for axis, mark in zip(AXES, grades):
        if mark < 0 or mark > 5:
            raise ValueError("mark outside 0-5 for axis " + axis)
        total += WEIGHT[axis] * mark
    return total


def gate_check(line):
    """Apply the bounty gate to one draft; raise with the reason it fails."""
    cleaned = line.strip()
    if line != cleaned:
        raise ValueError("draft carries stray whitespace at an edge")
    size = len(cleaned)
    if size < MIN_LEN or size > MAX_LEN:
        raise ValueError("draft runs %d characters; gate allows %d-%d" % (size, MIN_LEN, MAX_LEN))
    if "\n" in cleaned or "\r" in cleaned:
        raise ValueError("draft breaks across lines")
    if "  " in cleaned:
        raise ValueError("draft has a doubled space")
    lowered = cleaned.lower()
    for phrase in TIRED:
        if lowered.find(phrase) >= 0:
            raise ValueError("draft leans on a tired joke: " + phrase)


def pick_winner(drafts):
    """Score every gated draft and hand back the single best line."""
    seen = set()
    for line, _grades in drafts:
        if line in seen:
            raise ValueError("the same draft appears twice: " + line[:40])
        seen.add(line)
    scored = []
    for index, (line, grades) in enumerate(drafts):
        gate_check(line)
        scored.append((grade_draft(grades), -len(line), -index, line))
    scored.sort(reverse=True)
    best, runner_up = scored[0], scored[1]
    if best[0] == runner_up[0]:
        raise ValueError("top two drafts tie at %d points" % best[0])
    gap = best[0] - runner_up[0]
    if gap < 3:
        raise ValueError("winner leads by only %d points; rubric too close" % gap)
    return best[3]


def show_ranking(drafts):
    """Build the full ranking table, best first, for a human to check."""
    entries = []
    for line, grades in drafts:
        gate_check(line)
        entries.append((grade_draft(grades), len(line), line))
    entries.sort(key=lambda row: (-row[0], row[1]))
    table = ["pos score chars line"]
    for pos, (score, size, line) in enumerate(entries, start=1):
        table.append("%3d %5d %5d %s" % (pos, score, size, line))
    return "\n".join(table) + "\n"


def save_entry(line, target):
    """Write the line as bare UTF-8 bytes, then read back and hash it."""
    raw = line.encode("utf-8")
    folder = os.path.dirname(target)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(target, "wb") as handle:
        handle.write(raw)
    with open(target, "rb") as handle:
        stored = handle.read()
    if stored != raw:
        raise ValueError("entry file came back different from the winner")
    return hashlib.sha256(stored).hexdigest()


def main(argv=None):
    """Grade the drafts, crown the winner, and write the entry file."""
    parser = argparse.ArgumentParser(description="Pick the winning unsayable line and write entry.txt.")
    parser.add_argument("--out", default=DEFAULT_OUT, help="destination path for entry.txt")
    parser.add_argument("--ranking", action="store_true", help="print the full draft ranking to stderr first")
    opts = parser.parse_args(argv)
    if opts.ranking:
        sys.stderr.write(show_ranking(DRAFTS))
    winner = pick_winner(DRAFTS)
    fingerprint = save_entry(winner, opts.out)
    print(winner)
    print("sha256:", fingerprint)
    return None


if __name__ == "__main__":
    raise SystemExit(main())
