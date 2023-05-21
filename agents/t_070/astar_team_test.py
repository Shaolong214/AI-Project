# There is still room for improvement with this Astar agent, as there is no real g value (cost) for Azul, 
# so I have set two h values to find the best move. But I'm still working on the second h value
import heapq
import time, random
from Azul.azul_model import AzulGameRule as GameRule
from copy import deepcopy
import Azul.azul_utils as utils
import math

inf = math.inf
THINKTIME   = 1.65
NUM_PLAYERS = 2

# To solve the same f value and not supported between instances of 'AzulState' and 'AzulState' problem, make a self compare method
class HeapNode:
    def __init__(self, f, state, action):
        self.f = f
        self.state = state
        self.action = action

    def __lt__(self, other):
        return self.f < other.f
    
class myAgent():
    def __init__(self, _id):
        self.id = _id 
        self.game_rule = GameRule(NUM_PLAYERS) 

    def GetActions(self, state):
        return self.game_rule.getLegalActions(state, self.id)
    
    def calculate_g(self, action, state):
        
    # This h-heuristic is whether the selected and placed tiles will receive a higher adjacency score in subsequent walls
        if action[0] == utils.Action.TAKE_FROM_CENTRE or action[0] == utils.Action.TAKE_FROM_FACTORY:
            tile_grab = action[2]
            
            agent_state = state.agents[self.id]
            number_of_tiles = tile_grab.number
            pattern_line_dest = tile_grab.pattern_line_dest
            # Get the number of tiles already in the pattern line
            existing_tiles = agent_state.lines_number[pattern_line_dest]
            excess_tiles = number_of_tiles + existing_tiles - (pattern_line_dest + 1)
            excess_tiles = abs(5*excess_tiles)
            # Get the current grid state
            grid_state = agent_state.grid_state
            # Get the column where the tile will be placed
            tile_type = tile_grab.tile_type
            grid_col = int(agent_state.grid_scheme[pattern_line_dest][tile_type])
            # Calculate adjacency score
            adjacency_score = 0
            # Check if there's a adjacent tile on the left
            if grid_col > 0 and grid_state[pattern_line_dest][grid_col - 1] == 1:
                adjacency_score += 1
            # Check if there's a adjacent tile on the right
            if grid_col < agent_state.GRID_SIZE - 1 and grid_state[pattern_line_dest][grid_col + 1] == 1:
                adjacency_score += 1
            # Check if there's a adjacent tile above
            if pattern_line_dest > 0 and grid_state[pattern_line_dest - 1][grid_col] == 1:
                adjacency_score += 1
            # Check if there's a adjacent tile below
            if pattern_line_dest < agent_state.GRID_SIZE - 1 and grid_state[pattern_line_dest + 1][grid_col] == 1:
                adjacency_score += 1
            return 2*(excess_tiles + (4 - adjacency_score))

        return inf

    def calculate_h(self, action, state):
            
        # This h-heuristic is whether the selected and placed tiles will receive a higher adjacency score in subsequent walls
        if action[0] == utils.Action.TAKE_FROM_CENTRE or action[0] == utils.Action.TAKE_FROM_FACTORY:
            tile_grab = action[2]
            opponent_id = 1 - self.id
            agent_state = state.agents[opponent_id]
            number_of_tiles = tile_grab.number
            pattern_line_dest = tile_grab.pattern_line_dest
            # Get the number of tiles already in the pattern line
            existing_tiles = agent_state.lines_number[pattern_line_dest]
            excess_tiles = number_of_tiles + existing_tiles - (pattern_line_dest + 1)
            excess_tiles = abs(5*excess_tiles)
            # Get the current grid state
            grid_state = agent_state.grid_state
            # Get the column where the tile will be placed
            tile_type = tile_grab.tile_type
            grid_col = int(agent_state.grid_scheme[pattern_line_dest][tile_type])
            # Calculate adjacency score
            adjacency_score = 0
            # Check if there's a adjacent tile on the left
            if grid_col > 0 and grid_state[pattern_line_dest][grid_col - 1] == 1:
                adjacency_score += 1
            # Check if there's a adjacent tile on the right
            if grid_col < agent_state.GRID_SIZE - 1 and grid_state[pattern_line_dest][grid_col + 1] == 1:
                adjacency_score += 1
            # Check if there's a adjacent tile above
            if pattern_line_dest > 0 and grid_state[pattern_line_dest - 1][grid_col] == 1:
                adjacency_score += 1
            # Check if there's a adjacent tile below
            if pattern_line_dest < agent_state.GRID_SIZE - 1 and grid_state[pattern_line_dest + 1][grid_col] == 1:
                adjacency_score += 1
            return excess_tiles + (4 - adjacency_score)

        return inf
    

    def SelectAction(self, actions, rootstate):
        start_time = time.time()
         # Initialize heapq as priority queue.
        queue = [] 

        for action in actions:  
            g = self.calculate_g(action,rootstate)
            h = self.calculate_h(action,rootstate)
            f = g + h 
            next_state = self.game_rule.generateSuccessor(deepcopy(rootstate), action, self.id)
            heapq.heappush(queue, HeapNode(f, next_state, action))
            
        best_action = None
        best_f = None
        
        while len(queue) and time.time() - start_time < THINKTIME:  
                    
            node = heapq.heappop(queue)
            f, state, action = node.f, node.state, node.action

            if best_f is None or f < best_f:
                best_f = f
                best_action = action
                #print(f)

             # return a optimal solution when found       
            if f == 0:
                legal_actions = self.GetActions(deepcopy(state))
                if action in legal_actions:
                    #print("f == 0", action)
                    return action
                else:
                    next_state = deepcopy(state)
                    new_actions = self.GetActions(next_state)
                    for new_action in new_actions:
                        g = self.calculate_g(action,rootstate)
                        h = self.calculate_h(action,rootstate)
                        f = g + h 
                        next_state = self.game_rule.generateSuccessor(deepcopy(state), new_action, self.id)
                        heapq.heappush(queue, HeapNode(f, next_state, new_action))
            
        # print("Time up")
        # When time up, return a best solution
        if best_action is not None:
            #print("f != 0", best_action)
            return best_action
        else:
            #print("choosing a random action")
            return random.choice(actions)
 