from lzma import CHECK_CRC32
import random
from re import S
from typing import List
from enum import Enum, unique


kSuitColor = ['\u001b[37;1m', '\u001b[31m', '\u001b[32;1m', '\u001b[34;1m']
kSuits = ['♤', '♡', '♧', '♢']
kRanks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K']

def print_card(card_index: int) -> str:
    return '{}{}{}\u001b[0m'.format(kSuitColor[card_index // 13], kSuits[card_index // 13], kRanks[card_index % 13])

def print_cards(cards: List[int]) -> str:
    return ' '.join([print_card(card) for card in cards])





class State:
    def __init__(self):
        self.pre_flop_actions = []
        self.flop = [-1, -1, -1]
        self.flop_actions = []
        self.turn = -1
        self.turn_actions = []
        self.river = -1
        self.river_actions = []


@unique
class Action(Enum):
    FOLD = 1
    RAISE = 2  # RAISE 0 = check or call


class Player:
    def __init__(self, id):
        self.chips = 200
        self.hand = []
        self.id = id

    def take_action(self, state: State):
        pot = 0
        player_current_bet = [0] * 10
        if len(state.pre_flop_actions) == 0:
            print("You are the first on taking action")
        else:
            highest_bet = 0
            for (player_id, action, raise_amount) in state.pre_flop_actions:
                if action == Action.FOLD:
                    print('Player', player_id, 'FOLD', end=' ')
                else: # Action == RAISE
                    highest_bet += raise_amount
                    pot += highest_bet - player_current_bet[player_id]
                    player_current_bet[player_id] = highest_bet
                    if raise_amount == 0: 
                        print('Player', player_id, 'CALL to', highest_bet, end=' ')
                    else: # amount > 0
                        print('Player', player_id, 'RAISE', raise_amount, 'to', highest_bet, end=' ')
                
                print('(Total pot is {})'.format(pot))

        while True:
            action = input('Player {}: {} to call. Please enter your action (f = FOLD, c = CALL/CHECK, number = BET/RAISE):'.format(self.id, highest_bet - player_current_bet[self.id]))
            if action == 'f':
                return Action.FOLD, 0
            elif action == 'c':
                # TODO: computer call amount
                return Action.RAISE, 0
            elif action.isnumeric():
                # TODO: validate raise amount
                return Action.RAISE, int(action)
            else:
                print('Invalid input.')





class TexasHoldem:
    def __init__(self):
        self.num_of_players = 3
        self.players = [Player(id) for id in range(self.num_of_players)]
        self.dealer_pos = 0

    def play_one_hand(self):
        active_player = [True] * self.num_of_players
        active_player_count = self.num_of_players

        # Shuffle the card.
        deck = list(range(52))
        random.shuffle(deck)

        # Deal the card to players.
        for id, player in enumerate(self.players):
            player.hand = [deck.pop(), deck.pop()]
            print('Player', id, ':', print_cards(player.hand))

        state = State()
        # Pre-flop
        player_id = (self.dealer_pos + 3) % self.num_of_players
        small_blind_id = (self.dealer_pos + 1) % self.num_of_players
        big_blind_id = (self.dealer_pos + 2) % self.num_of_players
        stop_id = (self.dealer_pos + 3) % self.num_of_players
        state.pre_flop_actions.append((small_blind_id, Action.RAISE, 1))
        state.pre_flop_actions.append((big_blind_id, Action.RAISE, 1))
        while True:
            if active_player[player_id] == True:
                action, amount = self.players[player_id].take_action(state)
                state.pre_flop_actions.append((player_id, action, amount))
                if action == Action.FOLD:
                    active_player[player_id] = False
                    active_player_count -= 1
                elif action == Action.RAISE and amount > 0:
                    stop_id = player_id

            player_id = (player_id + 1) % self.num_of_players
            # Cycle completed with no one raise in previous round.
            if player_id == stop_id or active_player_count == 1:
                break

        if active_player_count == 1:
            # TODO: End of this hand
            pass

        # Flop
        state.flop = [deck.pop(), deck.pop(), deck.pop()]


        # Turn
        state.turn = deck.pop()

        # River
        state.river = deck.pop()




    