import time, random
from Azul.azul_model import AzulGameRule as GameRule
from copy import deepcopy
from collections import deque
import Azul.azul_utils as utils
from Azul.azul_model import AzulState
    

THINKTIME   = 0.9
NUM_PLAYERS = 2


# FUNCTIONS ----------------------------------------------------------------------------------------------------------#


# Defines this agent.
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
    
    def DoAction(self, state, action):
        score = state.agents[self.id].score
        newState = self.game_rule.generateSuccessor(state, action, self.id)
        newScore = newState.agents[self.id].score

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
            elif number_of_tiles == put_pattern_num: 
                return True
            
            # if not the 1st person pick up from center 
            elif not state.first_agent_taken:
                return True
            
            # if the new picked up tiles can exact full fill the left over spaces in any pattern line
            elif put_foor_num == 0  and number_of_tiles != put_pattern_num:
                for i in range(1,6):
                    if self.agent_state.lines_tile[i] == color_of_tiles:
                        currentFilled = self.agent_state.lines_number[i]
                        leftOver = patternLine_index - currentFilled
                        if leftOver   == number_of_tiles:
                            return True
            else:
                return False
        
        else:
            if newScore > score: # the score at each round is bigger than previous one
                return True
            else:
                return False

    
    def heuristicFunction(self, action):
        h = 0 
        return h 

    # Reference: So far the code below is using from example.bfs (Will modify afterward)
    # Start-----------------------------------------------------------
    def SelectAction(self, actions, rootstate):
        
        start_time = time.time()
        pathsList = []
        
        queue      = deque([]) 
        initial_state = deepcopy(rootstate)
        initial_Heuristic= self.heuristicFunction(rootstate)
        
        for initial_action in actions:
            initial_Node = (initial_state, initial_action, initial_Heuristic, pathsList)           
            queue.append(initial_Node)
            #goal =  self.DoAction(next_state, initial_action) 

        closed = []

        while len(queue) != 0 and time.time()-start_time < THINKTIME:

            currentNode = queue.popleft()
            currentState, currentAction, currentHeuristic, pathsList = currentNode 

            new_actions = self.GetActions(currentState) 
            
            for a in new_actions:

                if not any( target == currentState for target in closed):
                    closed.append(currentState)
                    
                    if currentHeuristic <= initial_Heuristic:
                        initial_state = currentState
                        
                        next_state = deepcopy(currentState)              
                        next_path  = pathsList + [a]                   
                        goal = self.DoAction(next_state, a) 
                
                        if goal:
                                print("path found:",next_path[0])
                                return next_path[0] 
                        else:
                            next_Heuristic = self.heuristicFunction(next_state)
                            queue.append((next_state, a, next_Heuristic, next_path)) 

        return random.choice(actions) 
    # End-----------------------------------------------------------------------
        
    
# END FILE -----------------------------------------------------------------------------------------------------------#
