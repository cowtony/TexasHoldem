from enum import Enum, unique
from typing import List, Tuple

@unique
class Action(Enum):
    # UNDEFINED = 0
    FOLD = 1
    CALL = 2   # Equivalent to `check`
    RAISE = 3  # Equivalent to `bet`


class State:
    def __init__(self, total_players: int, hand: tuple, id: int, player_id: int, actions: tuple):
        self.players = total_players
        self.my_hand = hand
        self.my_id = id
        self.current_player = player_id
        self.preflop_actions = actions

    def __str__(self):
        # TODO: implement this.
        color = f'\u001b[{31+self.my_id};1m'
        return f'{self.players} Player {self.my_id}: {self.my_hand} Actions: ' + ' '.join([f'{player}:{action.name}' for player, action in self.preflop_actions]) + '\u001b[0m'

    # For hash purpose, using this combining the Action could provide a correct hashable tuple.
    def getTuple(self):
        return (self.players, self.my_hand, self.my_id, self.current_player, self.preflop_actions)


    # Return the cost for action CALL or RAISE as well as the current pot size.
    # The cost will be the chip amount needed for this action.
    def getCost(self) -> Tuple[int, int, int]:
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
        return call_amount, call_amount + pot // 2, pot



def getActions(state: State) -> List[Action]:
    # TODO: Check preflop_actions to limit number of raise
    return [action for action in Action]