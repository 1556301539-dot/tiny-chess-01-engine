# tiny-chess-01-engine

[![make.fun · tiny-chess-01](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/1556301539-dot/tiny-chess-01-engine/rank.svg)](https://make.fun/bounty/tiny-chess-01/leaderboard)
[![reward](https://make.fun/badge/tiny-chess-01/1556301539-dot/tiny-chess-01-engine/reward.svg)](https://make.fun/bounty/tiny-chess-01)

A deterministic compact chess engine for the make.fun `tiny-chess-01` bounty. It parses FEN positions, generates legal moves, filters them through a fixed-depth alpha-beta search, and plays through the competition environment using only Python's standard library.

## Run it

```sh
MAKEFUN_ENV_URL=<environment-url> python3 main.py
```

Entered on [make.fun](https://make.fun/?ref=gw3x9y07&utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01).
