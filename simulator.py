from copy import copy, deepcopy
from typing import List, Tuple, Any
import queue
import matplotlib.pyplot as plt

from learning_agent import *
from game_state import *
from poker_deck import PokerDeck


class TexasHoldemSimulator:
    def __init__(self, agent_list: List[LearningAgent], verbose = 2):
        self.agents = agent_list
        self.chips = [0.0] * len(self.agents)
        self.dealer_id = 0   # Indicate who should talk first. small_blind = dealer + 1, big_blind = dealer + 2
        self.verbose = verbose


    # TODO: Implement a complete version for Texas Hold'em.
    def winningHand(self, hands: List[Tuple[int, int]], public_cards: tuple, deck: PokerDeck):
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


    # Return the winner IDs, it could be multiple winners split the pot.
    def showdown(self, exclusive_states: List[ExclusiveState], public_state: PublicState, active_players: List[int], deck: PokerDeck) -> List[int]:
        active_id = []
        active_hand = []
        for id in active_players:
            active_id.append(exclusive_states[id].my_id)
            active_hand.append(exclusive_states[id].my_hand)

        return [active_id[winner] for winner in self.winningHand(active_hand, public_state.cards, deck)]


    # A transaction deduct chips from player and add to the pot.
    # NOTE: The positive amount is flow into the pot.
    def updateChips(self, public_state, exclusive_states, player_id, amount):
        public_state.pot += amount
        exclusive_states[player_id].chips -= amount
        self.chips[player_id] -= amount


    def putBlinds(self, deck: PokerDeck, public_state: PublicState, exclusive_states: List[ExclusiveState]) -> None:
        small_blind_id = (self.dealer_id + 1) % len(self.agents)
        big_blind_id = (self.dealer_id + 2) % len(self.agents)
        
        # Small blind and Big blind putting their chips.
        public_state.preflop_actions = public_state.preflop_actions + ((small_blind_id, Action.RAISE),)  # Raise from 0 to 1
        self.updateChips(public_state, exclusive_states, small_blind_id, 1)
        if self.verbose == 2:
            print(f'Pot: {1}\t', end='')
            State(exclusive_states[small_blind_id], public_state).print(deck)
        
        public_state.preflop_actions = public_state.preflop_actions + ((big_blind_id, Action.RAISE),)  # Raise from 1 to 2
        self.updateChips(public_state, exclusive_states, big_blind_id, 2)
        if self.verbose == 2:
            print(f'Pot: {3}\t', end='')
            State(exclusive_states[big_blind_id], public_state).print(deck)


    # TODO: remove `deck` argument from here.
    def runPreFlop(self, deck: PokerDeck, public_state: PublicState, exclusive_states: List[ExclusiveState], active_players: queue.Queue):
        # Initilize players
        total_players = len(self.agents)
        stop_id = id = (self.dealer_id + 3) % total_players
        privious = [None] * total_players  # Store the previous state / action / reward for updating incorporateFeedback().

        while active_players.qsize() > 1:
            id = active_players.get()

            if privious[id] != None:  # Avoid the first call by checking Action
                self.agents[id].incorporateFeedback(privious[id][0], privious[id][1], privious[id][2], State(exclusive_states[id], public_state))
                
            action = self.agents[id].getAction(State(exclusive_states[id], public_state))
            call_cost, raise_cost, pot_size = State(exclusive_states[id], public_state).getCostBySimulation()
            if pot_size != public_state.pot:
                raise ("Some logical inside function State.getCostBySimulation()")  # type: ignore

            if action == Action.FOLD:
                privious[id] = (deepcopy(State(exclusive_states[id], public_state)), action, 0)
            elif action == Action.RAISE:
                stop_id = id  # The raise will refresh stop_id of the last player who eligible to talk.
                privious[id] = (deepcopy(State(exclusive_states[id], public_state)), action, -raise_cost)
                self.updateChips(public_state, exclusive_states, id, raise_cost)
                active_players.put(id)
            else:  # Action.CALL
                privious[id] = (deepcopy(State(exclusive_states[id], public_state)), action, -call_cost)
                self.updateChips(public_state, exclusive_states, id, call_cost)
                active_players.put(id)

            # Update public state.
            public_state.preflop_actions = public_state.preflop_actions + ((id, action),)

            # Print Info
            if self.verbose == 2:
                print(f'Pot: {pot_size}\t', end='') 
                State(exclusive_states[id], public_state).print(deck)

            id = (id + 1) % total_players
            if id == stop_id:
                break  # Preflp talk completed with no one raise in previous round.
        
        return privious


    def playOneHand(self) -> None:
        # Prepare the deck and shuffle it.
        deck = PokerDeck()

        # Deal the card to players. Initlize the start state for each agent.
        # NOTE: The order of dealing the card is not as real game. It shouldn't matter because the deck is shuffled.
        public_state = PublicState(len(self.agents))   # Only need one because it's shared information.
        exclusive_states = []                       # This will be different for each player.
        for id, agent in enumerate(self.agents):
            # NOTE: One simplfy is limited to only AA, KK, QQ
            card = deck.dealCard()
            exclusive_states.append(ExclusiveState(id, (card, card)))
            # exclusive_states.append(ExclusiveState(id, (deck.pop(), deck.pop())))
            if self.verbose == 2:
                print(f'Player_{id}:', deck.printCards(exclusive_states[-1].my_hand))

        active_players = queue.Queue()
        for id, agent in enumerate(self.agents):
            active_players.put(id)


        self.putBlinds(deck, public_state, exclusive_states)
        privious = self.runPreFlop(deck, public_state, exclusive_states, active_players)
        # TODO: run Flop
        # TODO: run Turn
        # TODO: run River

        # Calculate winner
        winners = self.showdown(exclusive_states, public_state, list(active_players.queue), deck)
        if self.verbose == 2:
            print(f'The winners are player {winners}')
        # One more update for the final reward
        for id in range(len(self.agents)):
            reward = public_state.pot / len(winners) if id in winners else 0
            if privious[id] != None:  # Some player may not doen a single action for the whole hand so the `previous` will be None.
                if self.verbose == 2:
                    print(privious[id][0], privious[id][1], privious[id][2] + reward)
                self.agents[id].incorporateFeedback(privious[id][0], privious[id][1], privious[id][2] + reward, None)
            self.updateChips(public_state, exclusive_states, id, -reward)
            
        
        if self.verbose == 2:
            print(f"Players' chips: {self.chips}\n")

        # Shift dealer position for next hand.
        self.dealer_id = (self.dealer_id + 1) % len(self.agents)


    def run(self, hands: int):
        history = []  # Store the chip history of agent_0 after each hand.
        for i in range(hands):
            self.playOneHand()
            history.append(deepcopy(self.chips[0]))
            if i % 1000 == 0:
                print(f'{i}/{hands} hands.')

        for id in range(len(self.agents)):
            print(f'Agent {id} has win rate: {self.chips[id] / hands * 100: .2f} bb/100.')

        plt.plot(history)
        plt.show()



# Return a single-element list containing a binary (indicator) feature
# for the existence of the (state, action) pair.  Provides no generalization.
def identityFeatureExtractor(state: State, action: Action) -> List[Tuple[Tuple[Any, Action], float]]:
    # NOTE: Do not directly put the State object into the tuple since it will use the object ID as hash key.
    # TODO: Not all attribute is extracted from state. Build a better feature extractor.
    featureKey = (state.exclusive.my_id, state.exclusive.my_hand, state.public.preflop_actions, action)
    featureValue = 1
    return [(featureKey, featureValue)]


def main():
    learning_agent = QLearningAgent(getActions, 1.0, identityFeatureExtractor)
    simulator = TexasHoldemSimulator([learning_agent, StochasticAgent()], verbose=0)
    simulator.run(100000)
    
    # Print the learned Q value regarding to state-action.
    if True:
        for feature, value in learning_agent.weights.items():
            print(f'{feature} {value}')
    print(f'Number of features: {len(learning_agent.weights)}')


if __name__ == "__main__":
    main()