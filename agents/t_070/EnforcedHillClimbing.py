import time, random
from Azul.azul_model import AzulGameRule as GameRule
from copy import deepcopy
from collections import deque
import Azul.azul_utils as utils
from Azul.azul_model import AzulState

import math
import heapq, random

inf = math.inf

THINKTIME   = 0.9
NUM_PLAYERS = 2


# FUNCTIONS ----------------------------------------------------------------------------------------------------------#


   
# The code below is modified & referenced from the sources below:
# [Source code]: https://github.com/COMP90054-2023S1/assignment1-BocongZhao823/blob/2cec9b32e89803b6869496e3268120c3b796dd59/util.py#L150
# Begin----------------------------------------
class Queue:
    """
      Implements a priority queue data structure. Each inserted item
      has a priority associated with it and the client is usually interested
      in quick retrieval of the lowest-priority item in the queue. This
      data structure allows O(1) access to the lowest-priority item.
    """
    def  __init__(self):
        self.heap = []
        self.count = 0

    def getMinimumPriority(self):
        return self.heap[0][0]

    def push(self, item, priority):
        entry = (priority, self.count, item)
        heapq.heappush(self.heap, entry)
        self.count += 1

    def pop(self):
        (_, _, item) = heapq.heappop(self.heap)
        return item

    def isEmpty(self):
        return len(self.heap) == 0
# End-----------------------------------------

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

    
    def heuristicFunction(self, action,state):
        if action != "ENDROUND" and action != "STARTROUND":
            agent_state = state.agents[self.id]
            tile_grab = action[2]
            number_of_tiles = tile_grab.number
            color_of_tiles = tile_grab.tile_type
            put_pattern_num = tile_grab.num_to_pattern_line
            patternLine_index = tile_grab.pattern_line_dest + 1
            factory_index = action[1] + 1
            put_foor_num = tile_grab.num_to_floor_line

            existing_tiles = agent_state.lines_number[patternLine_index - 1]

            if existing_tiles == 0:
                if number_of_tiles <= patternLine_index:
                    leftOver = patternLine_index - number_of_tiles
                    print(leftOver)
                    return abs(leftOver)
                else: 
                    print(put_foor_num)
                    return abs(put_foor_num)
            else:
                leftOver = patternLine_index - existing_tiles
                if number_of_tiles <= leftOver:
                    newLeftOver = leftOver - number_of_tiles
                    return abs(newLeftOver)
                else:
                    newfloor = number_of_tiles - leftOver
                    return  abs(newfloor)
        else:
            return inf

    # The code below is modified & referenced from the sources below:
    # Reference 1: Week2 search algorithmns lecture slides, page 41 & 42
    # Reference 2: aStarSearch() function in assignment 1
    # (link: https://github.com/COMP90054-2023S1/assignment1-BocongZhao823/blob/2cec9b32e89803b6869496e3268120c3b796dd59/search.py#L116)
    # Reference 3: My own work for assignment 1 task 1
    # (link: https://github.com/COMP90054-2023S1/assignment1-BocongZhao823/blob/2cec9b32e89803b6869496e3268120c3b796dd59/search.py#L143)
    # Reference 4: example.bfs 
    # (link: https://github.com/COMP90054-2023S1/A3_public_template/blob/3c89286e748ea39991a9cb27a64a1938cfe20eca/agents/t_XXX/example_bfs.py#L47)
    # Start-----------------------------------------------------------
    def SelectAction(self, actions, rootstate):
        
        start_time = time.time()
        pathsList = []
        
        #queue = deque([]) 
        queue = Queue()
        initial_state = deepcopy(rootstate)
        
        
        for initial_action in actions:
            initial_Heuristic= self.heuristicFunction(initial_action, rootstate)
            initial_Node = (initial_state, initial_action, initial_Heuristic, pathsList)     
            #queue.append(initial_Node)
            queue.push(initial_Node,initial_Heuristic)

        closed = []

        #while len(queue) != 0 and time.time() - start_time < THINKTIME:
        while queue.isEmpty() == False and time.time() - start_time < THINKTIME:

            #currentNode = queue.popleft()
            currentNode = queue.pop()

            currentState, currentAction, currentHeuristic, pathsList = currentNode 

            currentHeuristic = self.heuristicFunction(currentAction, currentState)

            # The code below reference from my work in assignment 1 task 1
            # [Source code]: https://github.com/COMP90054-2023S1/assignment1-BocongZhao823/blob/2cec9b32e89803b6869496e3268120c3b796dd59/search.py#L200
            # Begin--------------------------------------------------
            if not any( target == currentState for target in closed):
                    closed.append(currentState)
                    
                    if currentHeuristic < initial_Heuristic:
                        initial_state = currentState
                        break
            # End------------------------------------------------------
                    
                    # The code below reference from example.bfs
                    # [Source code]: https://github.com/COMP90054-2023S1/A3_public_template/blob/3c89286e748ea39991a9cb27a64a1938cfe20eca/agents/t_XXX/example_bfs.py#L54
                    # Begin------------------------------------
                    succState = self.get_success(currentState, currentAction)
                    new_actions = self.GetActions(succState) 
                    for a in new_actions:
                        succ_state_copy = deepcopy(succState)  
                        next_path  = pathsList + [a]                   
                        goal = self.DoAction(succ_state_copy, a) 
                
                        if goal == True:
                            print("path found:", a)
                            return a 
                        elif currentHeuristic == 0 :
                            print("h found: ", next_path[0])
                            return next_path[0] 
                    # End---------------------------------------

                        next_Heuristic = self.heuristicFunction(a, succ_state_copy)
                        next_node = succ_state_copy, a, next_Heuristic, next_path
                        #queue.append(next_node)
                        queue.push(next_node,next_Heuristic)
        
        randomPath = random.choice(actions)
        print("my path found", randomPath)
        return randomPath
    # End-----------------------------------------------------------------------
        
    
# END FILE -----------------------------------------------------------------------------------------------------------#
