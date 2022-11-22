# TexasHoldem
Reinforcement Learning

Run `simulator.py` to play.


## Simulator

- Support multiplayer (>= 2).
- Customize deck: Full deck or reduced deck.
  - One good example of reduced deck would be Q,K,A only and one card for each player.
    
    So that if a player get A, he should know he must win, if Q, he must lose, and K would be a 50/50 chance.
    
- Only implemented pre-flop, so there will NOT have the 5 public cards.
  - The comparision will reduce to only `pair > high_card`.


## Model

### States

- my_hand
- my_id
- preflop_actions

### Actions

- FOLD
- CALL (== CHECK)
- RAISE (== BET), always raise half pot.

## Algorithm

QLearing

## Simplfied assumptions:

- Player has infinite chips.

## Result

### AKQ single card Game

Run 10k hands, discount = 1.

- Against FoldAgent: 140 BB/100
- Against StochasticAgent: 60-100 BB/100
- Against CallAgent: 41-44 BB/100
- Against AKQAgent: 5.76, 9.66, -6.06, -5.83, 12.18 (120 states)



## TODO:

- Implement metric to count winning rate or total chips won. (done 11/21)
- Save and load the trainging result, so that human can play with a trained agent.