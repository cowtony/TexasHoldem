from enum import Enum, unique

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


  def IsEnd(self):
    return False


  def Utility(self):
    return 0




  def Successor(self, action: Action):
    return State(self.players, 
                 self.my_hand, 
                 self.my_id,
                (self.current_player + 1) % self.players, 
                 self.preflop_actions + [(self.current_player, action)])