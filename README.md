# Blackjack Game (Python + Pygame)

A Blackjack game with:
- Classic CLI gameplay mode
- Pygame frontend mode with animated card dealing
- Betting system with balance tracking
- `ALL IN` betting button

## Features

- Standard 52-card deck (shuffled each round)
- Blackjack hand value logic (Ace = 11 or 1 when needed)
- Dealer rule: dealer hits until at least 17
- Win/loss/tie detection, including bust checks
- Balance and per-round bet handling
- Pygame UI with:
  - `DEAL`, `HIT`, `STAND` buttons
  - `+`, `-`, and `ALL IN` betting controls
  - Card animations and chip graphics
  - Hidden dealer first card until reveal

## Requirements

- Python 3.8+
- `pygame`

Install pygame:

```bash
pip install pygame
```

## Run

From the project folder:

```bash
python game.py
```

You will be asked:

`Choose mode: [P]ygame or [C]LI (default P):`

- Press `Enter` for Pygame mode
- Type `c` for CLI mode

## How To Play

### Objective

Get a hand value closer to 21 than the dealer without going over 21.

### Card Values

- Number cards = face value
- J, Q, K = 10
- A = 11 (or 1 if 11 would cause bust)

### Round Flow

1. Set your bet (`+`, `-`, or `ALL IN`)
2. Press `DEAL`
3. Choose:
   - `HIT` to take another card
   - `STAND` to end your turn
4. Dealer plays automatically (hits below 17)
5. Balance updates after outcome:
   - Win: balance increases by bet
   - Loss: balance decreases by bet
   - Tie: balance unchanged

## Controls (Pygame)

- `DEAL`: start round
- `HIT`: draw one card
- `STAND`: end turn
- `+` / `-`: increase or decrease bet by 10
- `ALL IN`: set bet equal to full current balance

## Notes

- If `pygame` is not installed, the script falls back to CLI mode automatically.
- Game ends when balance reaches 0 (in pygame mode you can close the window to exit).
