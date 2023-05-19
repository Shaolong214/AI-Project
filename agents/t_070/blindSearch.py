import time, random
from Azul.azul_model import AzulGameRule as GameRule
from copy import deepcopy
from collections import deque
import Azul.azul_utils as utils
from Azul.azul_model import AzulState

import math

inf = math.inf

THINKTIME   = 0.9
NUM_PLAYERS = 2


# FUNCTIONS ----------------------------------------------------------------------------------------------------------#
# Reference 1: class myStack() class refers from Stack() class in COMP90054 assignment 1
# [Source code]: https://github.com/COMP90054-2023S1/assignment1-BocongZhao823/blob/2cec9b32e89803b6869496e3268120c3b796dd59/util.py#L133 
class myStack():
    def __init__(self):
        self.stack = []

    def push(self, state, action):
        node = state, action
        self.stack.append(node)

    def pop(self):
        if self.is_empty() != True:
            node = self.stack.pop()
            state, action = node
            return state, action 
        else:
            print("No node left over.")
    
    def is_empty(self):
        if len(self.stack) == 0:
            return True
        else:
            return False


class myAgent():
    def __init__(self, _id):
        self.id = _id
        self.game_rule = GameRule(NUM_PLAYERS) 
        self.agentState = AzulState.AgentState

    def GetActions(self, state):
        actions = self.game_rule.getLegalActions(state, self.id)
        return actions
    
    def get_success(self,state, action):
        state = self.game_rule.generateSuccessor(state, action, self.id)
        return state
    
    def checkGoal(self, state, action):
        if action != "ENDROUND" and action != "STARTROUND":
            tile_grab = action[2]
            number_of_tiles = tile_grab.number
            color_of_tiles = tile_grab.tile_type
            put_pattern_num = tile_grab.num_to_pattern_line
            patternLine_index = tile_grab.pattern_line_dest + 1
            factory_index = action[1] + 1
            put_foor_num = tile_grab.num_to_floor_line

            # if no tile put on floor
            if put_foor_num == 0 : 
                return True
            
            # if the number of picked up tiles is exact the same as the number of pattern line space in one row
            if number_of_tiles == put_pattern_num: 
                return True
            
            # if the new picked up tiles can exact full fill the left over spaces in any pattern line
            if put_foor_num == 0  and number_of_tiles != put_pattern_num:
                for i in range(1,6):
                    if self.agent_state.lines_tile[i] == color_of_tiles:
                        currentFilled = self.agent_state.lines_number[i]
                        leftOver = patternLine_index - currentFilled
                        if leftOver   == number_of_tiles:
                            return True
            else:
                return False
        
            
    # Reference List: 
    # Reference 1: Week2 search algorithmns lecture slides
    # Reference 2: example.bfs 
    # (link: https://github.com/COMP90054-2023S1/A3_public_template/blob/3c89286e748ea39991a9cb27a64a1938cfe20eca/agents/t_XXX/example_bfs.py#L47)
    # Start-----------------------------------------------------------
    
    def SelectAction(self, actions, rootstate):
        start_time = time.time()
        stackWhole = myStack() # DFS use Stack 
        closed = []
        goal = False
        for initial_action in actions:  
            stackWhole.push(rootstate, initial_action)
            while stackWhole.is_empty() != True and time.time() - start_time < THINKTIME:
                currentState, currentAction = stackWhole.pop()
                if currentState not in closed:
                    closed.append(currentState)
                    new_actions = self.GetActions(currentState) 
                    for action in new_actions:
                        goal = self.checkGoal(new_actions, action) 
                        if goal == False:
                            stackWhole.push(currentState, action)
                        else:
                            print("path",action)
                            return action
                    
        randomPath = random.choice(actions)
        print("random",randomPath)
        return randomPath
    # End-----------------------------------------------------------------------
        
    
# END FILE -----------------------------------------------------------------------------------------------------------#
