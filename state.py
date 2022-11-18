from enum import Enum, unique
from typing import List, Tuple

@unique
class Action(Enum):
    FOLD = 1
    CALL = 2   # Equivalent to `check`
    RAISE = 3  # Equivalent to `bet`


class State:
    def __init__(self, total_players: int, hand: list, id: int, player_id: int, actions: list):
        self.players = total_players
        self.my_hand = hand
        self.my_id = id
        self.current_player = player_id
        self.preflop_actions = actions


    # Return the cost for action CALL or RAISE.
    # The cost will be the chip amount needed for this action.
    def getCost(self) -> Tuple[int, int]:
        player_bet = [0] * self.players
        current_bet = 0
        pot = 0
        # Simulate completed actions to calculate pot size and current bet.
        for id, action in self.preflop_actions:
            if action == Action.RAISE:
                if pot == 0:
                    player_bet[id] = 1
                    current_bet = 1  # Small Blind
                    pot += 1
                elif pot == 1:
                    player_bet[id] = 2
                    current_bet = 2  # Big Blind
                    pot += 2
                else:
                    current_bet += pot // 2
                    pot += current_bet - player_bet[id]
                    player_bet[id] = current_bet
            elif action == Action.CALL:
                pot += current_bet - player_bet[id]
                player_bet[id] = current_bet
        
        call_amount = current_bet - player_bet[self.my_id]
        return call_amount, call_amount + pot // 2


    def IsEnd(self):
        raise("Not implemented")


    def Utility(self):
        raise("Not implemented")


    def Successor(self, action: Action):
        return State(self.players, 
                     self.my_hand, 
                     self.my_id,
                    (self.current_player + 1) % self.players, 
                     self.preflop_actions + [(self.current_player, action)])


def getActions(state: State) -> List[Action]:
    # TODO: Check preflop_actions to limit number of raise
    return [action for action in Action]