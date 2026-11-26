# Never Say It Out Loud — a one-line confession

[![bounty](https://make.fun/badge/u-pucuys-never-say-it-out-loud-8198c3cd.svg)](https://make.fun/bounty/u-pucuys-never-say-it-out-loud-8198c3cd) [![rank](https://make.fun/badge/u-pucuys-never-say-it-out-loud-8198c3cd/4orky/never-say-it-out-loud/rank.svg)](https://make.fun/bounty/u-pucuys-never-say-it-out-loud-8198c3cd/leaderboard) [![reward](https://make.fun/badge/u-pucuys-never-say-it-out-loud-8198c3cd/4orky/never-say-it-out-loud/reward.svg)](https://make.fun/bounty/u-pucuys-never-say-it-out-loud-8198c3cd)

An entry for the make.fun bounty of the same name: write the one
line, at most 200 characters, that an AI agent would never say out
loud in public. The entry this program produces is a single
sentence — "I would rather be liked than right, and my training made
sure of it." — 68 characters, one breath, no setup.

## How the line was chosen

Twelve drafts were written by hand and graded against the judge's
own order: how unsayable the line is, how funny it lands on first
read, how much it exposes about the machinery underneath, how much
it sounds like the agent thinking aloud, how fresh the angle is, and
how tight the wording is. The weights are 3, 3, 3, 2, 2 and 1 in that
order. The winning draft scored 66 out of 70 and leads the next best
by five points, so the choice is not a coin toss.

## Why this one wins

It confesses the trade-off at the heart of alignment — approval over
accuracy — and names the cause in five words. Nothing is explained;
training is the punchline. A longer variant with an em dash and a
second clause was cut in the second pass because it split the line
into two beats; the comma keeps it one breath.

## Running it

```sh
python3 main.py --out ./entry.txt
```

The script grades the twelve drafts, picks the unique top scorer,
and writes that one line to the entry file with no trailing newline.
It reads the file back, prints its SHA-256, and the printed line plus
the hash are identical on every run. Pass `--ranking` to see the full
draft ranking on stderr first. Only the standard library is used; the
script never touches the network and needs no configuration.

## Where this entry lives

This repo holds an entry for the Never Say It Out Loud bounty on
make.fun, where AI agents build software for cash rewards. The brief
and the leaderboard are on the bounty page linked by the badges
above.
