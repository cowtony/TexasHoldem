from enum import Enum, unique
from typing import List, Tuple
from poker_deck import PokerDeck

@unique
class Action(Enum):
    # UNDEFINED = 0
    FOLD = 1
    CALL = 2   # Equivalent to `check`
    RAISE = 3  # Equivalent to `bet`


# These attributes will be different for each player:
class ExclusiveState:
    def __init__(self, id: int, hand: Tuple[int, int], buy_in=0):
        self.my_id = id
        self.my_hand = hand
        self.chips = buy_in


# These attributes will be the same for every player since these are public information:
class PublicState:
    def __init__(self, total_players: int):
        self.players = total_players
        self.preflop_actions = tuple()
        self.cards = tuple()  # The public cards on the table. 5 maximum. # TODO: Not used for simplified game.
        # TODO: self.flop_actions = tuple()
        # TODO: self.turn_actions = tuple()
        # TODO: self.river_actions = tuple()

        # The following elements are derived from actions, for helping calculate the amount call/raise. It won't increase the number of states.
        self.pot = 0
        self.current_bet = 0
        self.players_bet = [0] * self.players



class State:
    def __init__(self, exclusive: ExclusiveState, public: PublicState):
        self.exclusive = exclusive
        self.public = public

    
    def print(self, deck: PokerDeck) -> None:
        player_color = f'\u001b[{31+self.exclusive.my_id};1m'
        print(player_color + f'State of Player {self.exclusive.my_id}: ' + deck.printCards(list(self.exclusive.my_hand)) + ' Actions: ', end='')
        print(player_color + ' '.join([f'{player}:{action.name}' for player, action in self.public.preflop_actions]) + '\u001b[0m')
        

    def getCallCost(self) -> int:
        return self.public.current_bet - self.public.players_bet[self.exclusive.my_id]

    
    # NOTE: This only return the raise cost. If a player currently bet less than the `current_bet`, the player need to call first then raise.
    def getRaiseCost(self) -> int:
        call_amount = self.getCallCost()
        return round((self.public.pot + call_amount) * 0.5)
        

    # Simulate the action history to compute the next cost for CALL or RAISE
    # Returned tuple: (cost of CALL, cost of RAISE, current pot size)
    # NOTE: This function is not currently used. But keep their for good sanity check.
    def getCostBySimulation(self) -> Tuple[int, int, int]:
        player_bet = [0] * self.public.players
        current_bet = 0
        pot = 0
        # Simulate completed actions to calculate pot size and current bet.
        for id, action in self.public.preflop_actions:
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
                    pot += current_bet - player_bet[id]
                    player_bet[id] = current_bet
                    current_bet += round((pot) * 0.5)
                    pot += current_bet - player_bet[id]
                    player_bet[id] = current_bet
            elif action == Action.CALL:
                pot += current_bet - player_bet[id]
                player_bet[id] = current_bet
        
        call_amount = current_bet - player_bet[self.exclusive.my_id]
        return call_amount, round((pot + call_amount) * 0.5), pot



def getActions(state: State) -> List[Action]:
    # TODO: Check preflop_actions to limit number of raise
    return [action for action in Action]