# IMPORTS AND CONSTANTS ----------------------------------------------------------------------------------------------#


import time, random
from Azul.azul_model import AzulGameRule as GameRule
from copy import deepcopy
from collections import deque
import Azul.azul_utils as utils
from Azul.azul_model import TilesRemaining
    

THINKTIME   = 0.9
NUM_PLAYERS = 2


# FUNCTIONS ----------------------------------------------------------------------------------------------------------#

# Reference: 
# 1. Week 7 lecture notebook (https://gibberblot.github.io/rl-notes/single-agent/MDPs.html)

class MDPAgent():

    def __init__(self, _id):
        self.id = _id 
        self.game_rule = GameRule(NUM_PLAYERS) 

    def get_states(self, state, action):
        state = self.game_rule.generateSuccessor(state, action, self.id)
        return state

    def get_actions(self,state):
        action = self.game_rule.getLegalActions(state, self.id)
        return action

    def get_transitions(self, state, action):
        transitions = []

        

    def get_reward(self, state, action, next_state):
        pass

    def is_terminal(self, state):
        if state.TilesRemaining() == True:  # End of round: if run out of tiles
            return True
        elif self.game_rule.gameEnds() == True: # End of game: if one row is filled with tiles
            return True
        else:
            return False

    def get_discount_factor(self):
        pass

    def get_initial_state(self):
        initialState = self.game_rule.initialGameState()
        return initialState
    
    def get_goal_states(self, action):
        pass       

# END FILE -----------------------------------------------------------------------------------------------------------#
