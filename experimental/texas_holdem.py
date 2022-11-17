from lzma import CHECK_CRC32
import random
from re import S
from typing import List
from enum import Enum, unique



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




    