from copy import copy, deepcopy
from typing import List, Tuple, Any
import matplotlib.pyplot as plt

from learning_agent import LearningAgent, StochasticAgent, CallOnlyAgent, HumanAgent, AKQAgent, QLearningAgent
from game_state import Action, State, getActions
from poker_deck import PokerDeck


class TexasHoldemSimulator:
    def __init__(self, agent_list: List[LearningAgent]):
        self.agents = agent_list
        self.chips = [0.0] * len(self.agents)
        self.chip_history = []  # Store the chip history of agent_0 after each hand.
        self.dealer_id = 0   # Indicate who should talk first. small_blind = dealer + 1, big_blind = dealer + 2


    # TODO: Implement a complete version for Texas Hold'em.
    def winningHand(self, hands: List[Tuple[int, int]], deck: PokerDeck):
        rank = []
        for card_1, card_2 in hands:
            num_1 = card_1 % len(deck.kRanks) + 1  # +1 to avoid 0 value.
            num_2 = card_2 % len(deck.kRanks) + 1
            if num_1 == num_2:  # Pair
                rank.append(num_1 * len(deck.kRanks) ** 2)
            elif num_1 > num_2:
                rank.append(num_1 * len(deck.kRanks) + num_2)
            else:  # num_1 < num_2
                rank.append(num_2 * len(deck.kRanks) + num_1)

        max_rank = max(rank)
        return [idx for idx, value in enumerate(rank) if value == max_rank]

    # Return the winner ID, it could be multiple winners split the pot.
    def showdown(self, states: List[State], active_player: List[bool], deck: PokerDeck) -> List[int]:
        active_id = []
        active_hand = []
        for state, active in zip(states, active_player):
            if active:
                active_id.append(state.my_id)
                active_hand.append(state.my_hand)

        return [active_id[winner] for winner in self.winningHand(active_hand, deck)]


    def play_one_hand(self) -> None:
        # Prepare the deck and shuffle it.
        deck = PokerDeck()

        # Initilize players
        total_players = len(self.agents)
        active_player = [True] * total_players
        active_player_count = total_players

        # Deal the card to players. Initlize the start state for each agent.
        # NOTE: The order of dealing the card is not as real game. It shouldn't matter because the deck is shuffled.
        states = []
        for id, agent in enumerate(self.agents):
            # NOTE: One simplfy is limited to only AA, KK, QQ
            card = deck.dealCard()
            states.append(State(total_players, (card, card), id, id, ()))
            # states.append(State(total_players, (deck.pop(), deck.pop()), id, id, ()))
            print(f'Player_{id}:', deck.printCards(states[-1].my_hand))

        # Store the previous state / action / reward for updating incorporateFeedback().
        privious = [(state, None, 0.0) for state in states]

        small_blind_id = (self.dealer_id + 1) % total_players
        big_blind_id = (self.dealer_id + 2) % total_players
        stop_id = id = (self.dealer_id + 3) % total_players

        # Small blind and Big blind putting their chips.
        for state in states:
            state.preflop_actions = state.preflop_actions + ((small_blind_id, Action.RAISE),)  # Raise from 0 to 1
        print(f'Pot: {1}\t', end='')
        states[small_blind_id].print(deck)
        self.chips[small_blind_id] += -1
        
        for state in states:
            state.preflop_actions = state.preflop_actions + ((big_blind_id, Action.RAISE),)  # Raise from 1 to 2
        print(f'Pot: {3}\t', end='')
        self.chips[small_blind_id] += -2
        states[big_blind_id].print(deck)

        # TODO: should we incorporateFeedBack for the force small blind and big blind?
        # self.agents[small_blind_id].incorporateFeedback(last_state[small_blind_id], Action.RAISE, -1, states[small_blind_id])
        # self.agents[ big_blind_id ].incorporateFeedback(last_state[ big_blind_id ], Action.RAISE, -2, states[ big_blind_id ])

        # Pre-flop
        while active_player_count > 1:
            if active_player[id] == True:
                if privious[id][1] != None:  # Avoid the first call by checking Action
                    self.agents[id].incorporateFeedback(privious[id][0], privious[id][1], privious[id][2], states[id])
                    
                action = self.agents[id].getAction(states[id])
                call_cost, raise_cost, pot_size = states[id].getCost()

                if action == Action.FOLD:
                    active_player[id] = False
                    active_player_count -= 1
                    privious[id] = (deepcopy(states[id]), action, 0)
                elif action == Action.RAISE:
                    stop_id = id  # The raise will refresh stop_id of the last player who eligible to talk.
                    self.chips[id] -= raise_cost
                    privious[id] = (deepcopy(states[id]), action, -raise_cost)
                    pot_size += raise_cost
                else:  # Action.CALL
                    self.chips[id] -= call_cost
                    privious[id] = (deepcopy(states[id]), action, -call_cost)
                    pot_size += call_cost

                # Update this action to each player's state
                for state in states:
                    state.preflop_actions = state.preflop_actions + ((id, action),)

                # Print Info
                print(f'Pot: {pot_size}\t', end='') 
                states[id].print(deck)

            id = (id + 1) % total_players
            if id == stop_id:
                break  # Preflp talk completed with no one raise in previous round.

        # TODO: Flop
        # TODO: Turn
        # TODO: River

        # Calculate winner
        winners = self.showdown(states, active_player, deck)
        print(f'The winners are player {winners}')
        # One more update for the final reward
        for id in range(total_players):
            reward = pot_size / len(winners) if id in winners else 0
            print(privious[id][0], privious[id][1], privious[id][2] + reward)
            self.agents[id].incorporateFeedback(privious[id][0], privious[id][1], privious[id][2] + reward, None)
            self.chips[id] += reward

        print(f"Players' chips: {self.chips}")
        self.chip_history.append(deepcopy(self.chips[0]))

        # Shift dealer position for next hand.
        self.dealer_id = (self.dealer_id + 1) % total_players


    def play_n_hands(self, n: int):
        for i in range(n):
            self.play_one_hand()



# Return a single-element list containing a binary (indicator) feature
# for the existence of the (state, action) pair.  Provides no generalization.
def identityFeatureExtractor(state: State, action: Action) -> List[Tuple[Tuple[Any, Action], float]]:
    featureKey = (state.getTuple(), action)
    featureValue = 1
    return [(featureKey, featureValue)]


def main():
    learning_agent = QLearningAgent(getActions, 1.0, identityFeatureExtractor)
    simulator = TexasHoldemSimulator([learning_agent, AKQAgent()])
    simulator.play_n_hands(10000)
    plt.plot(simulator.chip_history)
    plt.show()

    for (state, action), value in learning_agent.weights.items():
        print(f'{state} {action} {value}')
    print(len(learning_agent.weights))


if __name__ == "__main__":
    main()