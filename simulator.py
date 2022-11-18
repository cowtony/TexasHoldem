from typing import List
from rl_algorithm import *
from state import Action, State, getActions
import random


class TexasHoldemSimulator:
    def __init__(self, agent_list):
        self.agents = agent_list
        self.dealer_id = 0   # Indicate who should talk first. small_blind = dealer + 1, big_blind = dealer + 2

        # Standard Deck
        self.kSuitColor = ['\u001b[37;1m', '\u001b[31m', '\u001b[32;1m', '\u001b[34;1m']
        self.kSuits = ['♤', '♡', '♧', '♢']
        self.kRanks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K']

        # Leduc Deck (COmment out to use the standard deck)
        # self.kSuitColor = ['\u001b[37;1m']
        # self.kSuits = ['♤']
        # self.kRanks = ['A', 'T', 'J', 'Q', 'K']


    # Util function to print a card nicely.
    def printCard(self, card_index: int) -> str:
        return f'{self.kSuitColor[card_index // len(self.kRanks)]}{self.kSuits[card_index // len(self.kRanks)]} {self.kRanks[card_index % len(self.kRanks)]}\u001b[0m'


    # Util function to print a list of card. Normally used for printing player's hand.
    def printCards(self, cards: List[int]) -> str:
        return ' '.join([self.printCard(card) for card in cards])


    # Util function to print one state.
    def printState(self, state: State):
        print(f'State of Player {state.my_id}: ' + self.printCards(state.my_hand) + ' Actions: ', end='')
        print(' '.join([f'{player}:{action.name}' for player, action in state.preflop_actions]))


    def checkWinner(self, states: List[State]):
        print('CheckWinner')


    def showdown(self, states):
        print('ShowDown')


    def play_one_hand(self):
        # Prepare the deck and shuffle it.
        deck = list(range(len(self.kSuits) * len(self.kRanks)))
        random.shuffle(deck)

        # Initilize players
        total_players = len(self.agents)
        active_player = [True] * total_players
        active_player_count = total_players

        # Deal the card to players. Initlize the start state for each agent.
        # NOTE: The order of dealing the card is not as real game. It shouldn't matter because the deck is shuffled.
        states = []
        for id, agent in enumerate(self.agents):
            states.append(State(total_players, [deck.pop(), deck.pop()], id, id, []))
            print(f'Player_{id}:', self.printCards(states[-1].my_hand))
        last_state = [None] * total_players
        last_action = [None] * total_players

        small_blind_id = (self.dealer_id + 1) % total_players
        big_blind_id = (self.dealer_id + 2) % total_players
        current_id = (self.dealer_id + 3) % total_players
        stop_id = (self.dealer_id + 3) % total_players

        # Small blind and Big blind putting their chips.
        for state in states:
            state.preflop_actions.append((small_blind_id, Action.RAISE))  # Raise from 0 to 1
            state.preflop_actions.append((big_blind_id, Action.RAISE))  # Raise from 1 to 2
            self.printState(state)

        # Pre-flop
        while True:
            if active_player[current_id] == True:
                self.agents[current_id].incorporateFeedback('self', last_state[current_id], last_action[current_id], 0, states[current_id])
                last_action[current_id] = self.agents[current_id].getAction('self', states[current_id])  # TODO: Why I have to add a self arg here???????????????????????????????
                last_state[current_id] = states[current_id]
                
                # Update this action to each player's state
                for state in states:
                    state.preflop_actions.append((current_id, last_action[current_id]))
                    self.printState(state)

                if last_action[current_id] == Action.FOLD:
                    active_player[current_id] = False
                    active_player_count -= 1
                    if active_player_count == 1:
                        self.checkWinner(states)
                        break
                elif last_action[current_id] == Action.RAISE:
                    stop_id = current_id  # The raise will refresh stop_id of the last player who eligible to talk.
                else:  # Action.CALL
                    amount = states[current_id].getCallAmount()
                    pass

            current_id = (current_id + 1) % total_players
            if current_id == stop_id:
                break  # Preflp talk completed with no one raise in previous round.



        # TODO: Flop
        # TODO: Turn
        # TODO: River

        # TODO: Calculate winner
        self.showdown(states)



# Return a single-element list containing a binary (indicator) feature
# for the existence of the (state, action) pair.  Provides no generalization.
def identityFeatureExtractor(state: State, action: Action) -> List[Tuple[Tuple, int]]:
    featureKey = (state, action)
    featureValue = 1
    return [(featureKey, featureValue)]

def main():
    learning_agent = QLearningAgent(getActions, 1.0, identityFeatureExtractor)
    simulator = TexasHoldemSimulator([StochasticAgent, StochasticAgent])
    simulator.play_one_hand()


if __name__ == "__main__":
    main()