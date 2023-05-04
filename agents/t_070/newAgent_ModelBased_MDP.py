# IMPORTS AND CONSTANTS ----------------------------------------------------------------------------------------------#


import time, random
from Azul.azul_model import AzulGameRule as GameRule
from copy import deepcopy
from collections import deque
import Azul.azul_utils as utils
from Azul.azul_model import TilesRemaining
from Azul.azul_model import AgentState
    

THINKTIME   = 0.9
NUM_PLAYERS = 2


# FUNCTIONS ----------------------------------------------------------------------------------------------------------#

# Reference: 
# 1. Week 7 lecture notebook (https://gibberblot.github.io/rl-notes/single-agent/MDPs.html)

class MDPAgent():

    def __init__(self, _id):
        self.id = _id 
        self.game_rule = GameRule(NUM_PLAYERS) 
        self.agentState = AgentState()

    def get_states(self, state, action):
        state = self.game_rule.generateSuccessor(state, action, self.id)
        return state

    def get_actions(self,state):
        action = self.game_rule.getLegalActions(state, self.id)
        return action
    
    # I feel the transitions is mainly about 2 actions (pick from factory or center)
    # 
    def get_transitions(self, state, action):
        transitions = []

        
    def valid_add(self, state, newState, newAction, prob = 1.0):
        if newAction in self.get_actions(state):
            return True
        else:
            return False

    # I feel the reward should consider all the situations
    # 1) complete a row/column/set 2) get closed tiles 3) deletion mark etc
    # The reward is calculated at the round end
    # However, I decide to start with a simple version
    # The reward will given once reach the goal
    def get_reward(self, state, action, next_state):
        #reward = self.agentState
        reward = 0
        if self.get_goal_states() == True:
            reward += 10
        else:
            reward = 0
        #reward = self.agentState.ScoreRound()
        return reward

    def is_terminal(self, state):
        if state.TilesRemaining() == True:  # End of round: if run out of tiles
            return True
        elif self.game_rule.gameEnds() == True: # End of game: if one row is filled with tiles
            return True
        else:
            return False

    def get_discount_factor(self):
        discount = 1
        return discount

    def get_initial_state(self):
        initialState = self.game_rule.initialGameState()
        return initialState
    
    # Start with a simple reasonable goal (might change afterwards)
    # My goal is if any column or row or set is full filled with tiles
    def get_goal_states(self):
        if self.agentState.GetCompletedRows() or  self.agentState.GetCompletedColumns() or self.agentState.GetCompletedSets():
            return True
        else:
            False


class valueIter(MDPAgent):
    pass

# END FILE -----------------------------------------------------------------------------------------------------------#
