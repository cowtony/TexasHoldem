from state import Action, State
from typing import Tuple


class Agent:
  """
  An agent must define a getAction method, but may also define the
  following methods which will be called if they exist:

  def registerInitialState(self, state): # inspects the starting state
  """
  def __init__(self, player_id=0):
    self.player_id = player_id

  def getAction(self, state: State) -> Action:
    """
    The Agent will receive a GameState (from either {pacman, capture, sonar}.py) and
    must return an action from Directions.{North, South, East, West, Stop}
    """
    raise NotImplementedError("Override me")


class HumanAgent(Agent):
  def getAction(self, state: State) -> Action:
    while True:
      action = input(f"Player_{state.my_id}, What's your action? 1:FOLD 2:CALL/CHECK 3:RAISE  ")
      if action == '1':
        return Action.FOLD
      elif action == '2':
        return Action.CALL
      elif action == '3':
        return Action.RAISE
      else:
        print('Invalid input!')


class FoldOnlyAgent(Agent):
  def getAction(self, state: State) -> Action:
    return Action.FOLD


class CallOnlyAgent(Agent):
  def getAction(self, state: State) -> Action:
    return Action.CALL


class LearningAgent(Agent):

  def Value(self, state: State) -> Tuple[float, Action]:
    if state.IsEnd():
      return state.Utility(), None

    if state.current_player == self.player_id:
      max_value, best_action = float('-inf'), None
      for action in self.GetActions(state):
        value, _ = self.Value(state.Successor(action))
        if value > max_value:
          max_value, best_action = value, action
      return max_value, best_action

    else:
      sum_value = 0
      for action in self.GetActions(state):
        value, _ = self.Value(state.Successor(action))
        sum_value += value * (1/action)  # TODO: learn PI(state, action)
      return sum_value, None


  def GetActions(self, state: State):
    return [Action.FOLD, Action.CALL, Action.RAISE]


  def getAction(self, state: State) -> Action:
    if state.IsEnd():
      return None

    value, action = self.Value(state)

    
    return action
      