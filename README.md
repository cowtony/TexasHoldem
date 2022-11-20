# TexasHoldem
Reinforcement Learning

Run `simulator.py` to play.


## Simulator

- Support multiplayer (>= 2)
- Customize deck: Full deck or reduced deck.
  - One good example of reduced deck would be Q,K,A only and one card for each player.
    
    So that if a player get A, he should know he must win, if Q, he must lose, and K would be a 50/50 chance.
    
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