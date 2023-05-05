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
# Week 7 lecture notebook (https://gibberblot.github.io/rl-notes/single-agent/MDPs.html)
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
    def get_transitions(self, state, action):
        transitions = []

        # I feel that I have checked my actions are legal action, thus, it would also be "valid_add" 
        action = self.get_actions(state)

        if action == "ENDROUND":
            pass
        elif action == "STARTROUND":
            pass 
        elif action[0] == utils.Action.TAKE_FROM_FACTORY:
            # after take action: pick tiles from factory
            # it need to get all x number of y colored tile from factory z & put on ith line or floor or bag
            # E.g., "Agent 1 takes 1 yellow(Y) tiles from factory1 1Y placed in pattern line 1"
            tile_grab = action[2]
            number_of_tiles = tile_grab.number
            color_of_tiles = tile_grab.tile_type
            transitions += self.valid_add(state)

        elif action[0] == utils.Action.TAKE_FROM_CENTRE:
            transitions += self.valid_add(state)
        
        return transitions
    
    # So far prob for each state = 1
    #def valid_add(self, state):
        #newAction = self.get_actions(state)
        #newState = self.get_states(state, newAction)
        #tile_grab = newAction[2]
        #number_of_tiles = tile_grab.number
        #color_of_tiles = tile_grab.tile_type
        #if action in self.get_actions(state):
        #    pass

        
        return state

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


# Reference: 
# Week 7 lecture notebook (https://gibberblot.github.io/rl-notes/single-agent/value-iteration.html)
class valueIter():

    def __init__(self, _id, values):
        self.mdp = MDPAgent()
        self.values = values
    
    def bellmanEqu(self, state, action, new_state):
        prob = 1.0
        reward = self.mdp.get_reward(state, action, new_state)
        discount = self.mdp.get_discount_factor()
        new_value += prob * (reward + discount * self.values.get_value(new_state)) 
    
    def value_iteration(self, max_iterations = 100, theta = 0.001):
        for i in range(max_iterations):
            delta = 0.0
            new_values = 0

            for state in self.mdp.get_states():
                qtable = None
                for action in self.mdp.get_actions():
                    new_value = 0.0
                    for new_state in self.mdp.get_transitions(state, action):
                        new_value += self.bellmanEqu(self, state, action, new_state)
                         


# END FILE -----------------------------------------------------------------------------------------------------------#
