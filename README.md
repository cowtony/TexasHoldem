# TexasHoldem
Reinforcement Learning

Run `simulator.py` to play.


## Simulator

- Support multiplayer (>= 2)
- Customize deck: Full deck or reduced deck.
- Only implemented pre-flop, so there will NOT have the 5 public cards.
  - The comparision will reduce to only `pair > high_card`.


## Model

### States

### Actions

- FOLD
- CALL (== CHECK)
- RAISE (== BET), always raise half pot.

## Algorithm


## Simplfied assumptions:

- Player has infinite chips.


## TODO:

- Implement metric to count winning rate or total chips won.