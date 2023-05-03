# IMPORTS AND CONSTANTS ----------------------------------------------------------------------------------------------#


import time, random
from Azul.azul_model import AzulGameRule as GameRule
from copy import deepcopy
from collections import deque
import Azul.azul_utils as utils
    

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

    def get_actions(self,state):
        return self.game_rule.getLegalActions(state, self.id)

    def get_transitions(self, state, action):
        transitions = []
        

    def get_reward(self, state, action, next_state):
        pass

    def is_terminal(self, state):
        pass

    def get_discount_factor(self):
        pass

    def get_initial_state(self):
        pass

    def get_goal_states(self, action):
        pass        
    
# END FILE -----------------------------------------------------------------------------------------------------------#
