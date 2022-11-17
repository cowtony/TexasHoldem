from reference.mdp import MDP
from enum import Enum, unique

@unique
class Action(Enum):
    FOLD = 1
    CALL = 2   # Equivalent to `check`
    RAISE = 3  # Equivalent to `bet`

class TexasHoldemMDP(MDP):
    # TODO: rewrite the INIT.
    def __init__(self, n=5): 
        self.n = n
        self.hand_cards = [5,6]


    def startState(self):
        # 
        return (self.hand_cards, [])  # Action list


    def actions(self, state):
        # TODO: All 3 action should be valid at any state, however if we want to limit the number of RAISE, we might need the input state.
        return [Action.FOLD, Action.CALL, Action.RAISE]


    def succAndProbReward(self, state, action):
        return [(state, 0.4, 0),
                (min(max(state + action, -self.n), +self.n), 0.6, state)]


    def discount(self):
        return 1.0
