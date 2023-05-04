import heapq
import time, random
from Azul.azul_model import AzulGameRule as GameRule
from copy import deepcopy
import Azul.azul_utils as utils

THINKTIME   = 1
NUM_PLAYERS = 2

# To solve the same f value and not supported between instances of 'AzulState' and 'AzulState'" problem, make a self compare
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
        # Make the number of tiles taken match the pattern empty space that can be put as closely as possible 
        if action[0] == utils.Action.TAKE_FROM_CENTRE or action[0] == utils.Action.TAKE_FROM_FACTORY:
            # if acton is ENDROUND Then return big value
            tile_grab = action[2]
            number_of_tiles = tile_grab.number
            pattern_line_dest = tile_grab.pattern_line_dest
            # Get the number of tiles already in the pattern line
            agent_state = state.agents[self.id]
            existing_tiles = agent_state.lines_number[pattern_line_dest]
            excess_tiles = number_of_tiles + existing_tiles - (pattern_line_dest + 1)
            return abs(excess_tiles)
        return 9999

    def calculate_h(self, action):
    
        # This h value will be optimized later, e.g. The first pattern has a higher priority than the second line and so on
        if action[0] == utils.Action.TAKE_FROM_CENTRE or action[0] == utils.Action.TAKE_FROM_FACTORY:
            tile_grab = action[2]
            number_of_tiles = tile_grab.number
            pattern_line_dest = tile_grab.pattern_line_dest
            #print(action,pattern_line_dest)
            tiles_required = (pattern_line_dest+1)
            return abs(tiles_required)
        return 9999


    def SelectAction(self, actions, rootstate):
        start_time = time.time()
        queue = []  # Initialize heapq as priority queue.

        for action in actions:  
            g = self.calculate_g(action,rootstate)
            h = self.calculate_h(action)
            f = g 
            next_state = self.game_rule.generateSuccessor(deepcopy(rootstate), action, self.id)
            heapq.heappush(queue, HeapNode(f, next_state, action))
            
        best_action = None
        best_f = None
        
        while len(queue) and time.time() - start_time < THINKTIME:  
            # Break out of the loop when time is up
                
        
            node = heapq.heappop(queue)
            f, state, action = node.f, node.state, node.action

            if best_f is None or f < best_f:
                best_f = f
                best_action = action

             # return a optimal solution when found       
            if f == 0 : 
                print("f == 0", action)
                return action
            else:
                next_state = deepcopy(state)
                new_actions = self.GetActions(next_state)
                for new_action in new_actions:
                    g = self.calculate_g(new_action,next_state)
                    h = self.calculate_h(new_action)
                    f = g 
                    next_state = self.game_rule.generateSuccessor(deepcopy(state), new_action, self.id)
                    heapq.heappush(queue, HeapNode(f, next_state, new_action))
                    
        print("Time up")

        # When time up, return a best solution
        if best_action is not None:
            print("f != 0", best_action)
            return best_action
        else:
            print("queue is empty, choosing a random action")
            print(random.choice(actions))
            return random.choice(actions)
 