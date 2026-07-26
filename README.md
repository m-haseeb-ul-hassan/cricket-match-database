# Cricket Match Database

A main-memory database for cricket match records, built entirely on self-balancing binary search trees. Matches are stored in an AVL tree keyed by match ID, and each individual match holds its own two nested AVL trees, one per team, tracking the cricketers who played in it.

## Why AVL, and why nested

A plain BST degrades to O(n) lookups if match IDs come in sorted or near-sorted order (e.g. inserting PSL1-1, PSL1-2, PSL1-3... in sequence). Keeping the match tree height-balanced guarantees O(log n) add/find/delete regardless of insertion order.

The nesting is the more interesting design choice: every `Match` node in the outer tree owns two more AVL trees (`t1_players`, `t2_players`) for its own cricketers. This means cricketer lookups within a match, and rebalancing after a roster change, never touch the outer match tree at all, the two structures are fully decoupled.

## Features

- **Match ID parsing** — IDs like `PSL2-1`, `PSL10-4` are parsed into `(league name, league number, match number)` so that league numbers sort numerically instead of lexicographically (`PSL2` before `PSL10`, not after).
- **Match operations** — add, delete, find, and print all matches in sorted (in-order) order.
- **Cricketer operations** — add/delete a cricketer to either team in a given match, and find every match a given cricketer played in (returns a new `CricketDatabase` built from the matches found).
- **Self-balancing** — every insert/delete on both the match tree and the player trees triggers the standard AVL rotation logic (LL, RR, LR, RL) to keep height balanced.
- **Balance diagnostics** — `isBSTBalanced()` checks whether the current match tree is height-balanced; `balanceTree()` rebuilds a balanced tree from a sorted in-order collection of existing matches.
- **Persistence (bonus)** — `save_to_file()` / `load_from_file()` serialize the full database, including each match's player rosters, to and from a plain text file (`matches.txt`), so data survives across runs.

## Structure

```
DSA-Assignment03-BST.py
```

Single-file implementation, containing:
- `parse_id()` — match ID parser for correct BST ordering
- `PNode` / `PlayerBST` — AVL tree of cricketer names, one instance per team per match
- `Match` — a match record, owning its two `PlayerBST` instances
- `MNode` / `CricketDatabase` — the outer AVL tree of matches, keyed by parsed match ID
- CLI menu (`__main__` block) for interactive use

## Run it

```
python DSA-Assignment03-BST.py
```

You'll get a menu-driven interface:
```
1. Add Match
2. Delete Match
3. Find Match
4. Print All Matches
5. Add Cricketer
6. Delete Cricketer
7. Find Matches by Cricketer
8. Is Balanced BST
9. Balance Tree
10. Save and Exit
```

Match IDs should follow the `LEAGUE<number>-<matchNumber>` format, e.g. `PSL1-1`.

## Course context

Built for **Data Structures and Algorithms (COMP 200-A)**, Assignment 3, Forman Christian College University.

**Status:** Complete.
