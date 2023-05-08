import time, random
from Azul.azul_model import AzulGameRule as GameRule
from copy import deepcopy
from collections import deque
import Azul.azul_utils as utils
import heapq
from Azul.azul_model import AzulState
    

THINKTIME   = 0.9
NUM_PLAYERS = 2


# FUNCTIONS ----------------------------------------------------------------------------------------------------------#

class myAgent():

    # Reference 1: example_bfs.py
    def __init__(self, _id):
        self.id = _id
        self.game_rule = GameRule(NUM_PLAYERS) 
        self.agentState = AzulState.AgentState()

    def GetActions(self, state):
        return self.game_rule.getLegalActions(state, self.id)
    
    def get_successor(self, state, action):
        state = self.game_rule.generateSuccessor(state, action, self.id)
        return state
    
    def get_initial_state(self):
        initialState = self.game_rule.initialGameState()
        return initialState
        
    def get_goal_states(self, state):
        action =  self.game_rule.getLegalActions(state, self.id)
        tile_grab = action[2]
        number_of_tiles = tile_grab.number
        #color_of_tiles = tile_grab.tile_type
        put_pattern_num = tile_grab.num_to_pattern_line
        #patternLine_index = tile_grab.pattern_line_dest + 1
        #factory_index = action[1] + 1
        if self.agentState.GetCompletedRows() or  self.agentState.GetCompletedColumns() or self.agentState.GetCompletedSets():
            return True 
        elif number_of_tiles == put_pattern_num:
            return True
        else:
            return False
        
    def heuristicFunction(self, state):
        pass

    def SelectAction(self, action, rootstate, heuristic):
    
# END FILE -----------------------------------------------------------------------------------------------------------#
