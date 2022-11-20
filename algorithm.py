import random
import math
from collections import defaultdict
from typing import List, Tuple, Dict, Any, Callable

from game_state import State, Action


# Abstract class: an RLAlgorithm performs reinforcement learning.  All it needs
# to know is the set of available actions to take.  The simulator (see
# simulate()) will call getAction() to get an action, perform the action, and
# then provide feedback (via incorporateFeedback()) to the RL algorithm, so it can adjust
# its parameters.
class RLAlgorithm:
    # Your algorithm will be asked to produce an action given a state.
    def getAction(self, state: State) -> Action: raise NotImplementedError("Override me")

    # We will call this function when simulating an MDP, and you should update
    # parameters.
    # If |state| is a terminal state, this function will be called with (s, a,
    # 0, None). When this function is called, it indicates that taking action
    # |action| in state |state| resulted in reward |reward| and a transition to state
    # |newState|.
    def incorporateFeedback(self, state: State, action: Action, reward: float, newState: State): pass


class StochasticAgent(RLAlgorithm):
    def getAction(self, state: State) -> Action:
      return random.choice([action for action in Action])


class FoldOnlyAgent(RLAlgorithm):
    def getAction(self, state: State) -> Action:
        return Action.FOLD


class CallOnlyAgent(RLAlgorithm):
    def getAction(self, state: State) -> Action:
        return Action.CALL


class RaiseOnlyAgent(RLAlgorithm):
    def getAction(self, state: State) -> Action:
        return Action.RAISE


class HumanAgent(RLAlgorithm):
    def getAction(self, state: State) -> Action:
        while True:
            action = input(f"Player_{state.my_id}, What's your action (1:FOLD 2:CALL/CHECK 3:RAISE)? ")
            if action == '1':
                return Action.FOLD
            elif action == '2':
                return Action.CALL
            elif action == '3':
                return Action.RAISE
            else:
                print('Invalid input!')


# Performs Q-learning.  Read util.RLAlgorithm for more information.
# actions: a function that takes a state and returns a list of actions.
# discount: a number between 0 and 1, which determines the discount factor
# featureExtractor: a function that takes a state and action and returns a list of (feature name, feature value) pairs.
# explorationProb: the epsilon value indicating how frequently the policy
# returns a random action
class QLearningAgent(RLAlgorithm):
    def __init__(self, actions: Callable, discount: float, featureExtractor: Callable, explorationProb=0.2):
        self.actions = actions
        self.discount = discount
        self.featureExtractor = featureExtractor
        self.explorationProb = explorationProb
        self.weights = defaultdict(float)
        self.numIters = 1  # Starting from 1 to avoid divided by zero in `getStepSize()`


    # Return the Q function associated with the weights and features
    def getQ(self, state: State, action: Action) -> float:
        score = 0
        for feature, value in self.featureExtractor(state, action):
            score += self.weights[feature] * value
        return score


    # This algorithm will produce an action given a state.
    # Here we use the epsilon-greedy algorithm: with probability
    # |explorationProb|, take a random action.
    def getAction(self, state: State) -> Action:
        self.numIters += 1
        if random.random() < self.explorationProb:
            return random.choice(self.actions(state))
        else:
            return max([(self.getQ(state, action), action) for action in self.actions(state)], key=lambda tup: tup[0])[1]


    # Call this function to get the step size to update the weights.
    def getStepSize(self) -> float:
        return 1.0 / math.sqrt(self.numIters)


    # We will call this function with (s, a, r, s'), which you should use to update |weights|.
    # Note that if s is a terminal state, then s' will be None.  Remember to check for this.
    # You should update the weights using self.getStepSize(); use
    # self.getQ() to compute the current estimate of the parameters.
    def incorporateFeedback(self, state: State, action: Action, reward: float, newState: State) -> None:
        eta = self.getStepSize()
        q_opt = self.getQ(state, action)
        v_opt = 0 if newState is None \
                  else max(self.getQ(newState, act) for act in self.actions(newState))
        coefficient = eta * (q_opt - (reward + self.discount * v_opt))

        for feature, value in self.featureExtractor(state, action):
            self.weights[feature] -= coefficient * value

