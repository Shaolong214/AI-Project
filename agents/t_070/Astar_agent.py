import heapq
import time, random
from Azul.azul_model import AzulGameRule as GameRule
from copy import deepcopy
from collections import deque
import Azul.azul_utils as utils


THINKTIME   = 1.8
NUM_PLAYERS = 2


class myAgent():
    def __init__(self, _id):
        self.id = _id 
        self.game_rule = GameRule(NUM_PLAYERS) 

    def GetActions(self, state):
        return self.game_rule.getLegalActions(state, self.id)
    
    def calculate_g(self, action):
        # This g value will optimisation later, eg The first pattern has a higher priority than the second line and so on
        if action[0] == utils.Action.TAKE_FROM_CENTRE or action[0] == utils.Action.TAKE_FROM_FACTORY:
            tile_grab = action[2]
            number_of_tiles = tile_grab.number
            pattern_line_dest = tile_grab.pattern_line_dest

            excess_tiles = number_of_tiles - (pattern_line_dest + 1)
            return abs(excess_tiles)
        return 0

    def calculate_h(self, action):
        # Make the number of tiles taken match the pattern as closely as possible 
        if action[0] == utils.Action.TAKE_FROM_CENTRE or action[0] == utils.Action.TAKE_FROM_FACTORY:
            tile_grab = action[2]
            number_of_tiles = tile_grab.number
            pattern_line_dest = tile_grab.pattern_line_dest

            tiles_required = (pattern_line_dest + 1) - number_of_tiles
            return abs(tiles_required)
        return 0


    def SelectAction(self, actions, rootstate):
        start_time = time.time()
        queue = []  # Initialize heapq as priority queue.
        index = 0  # This index is used as a second priority attribute when have two same f value actions
        
        for action in actions:
            
            g = self.calculate_g(action)
            h = self.calculate_h(action)
            f = g + h
            next_state = self.game_rule.generateSuccessor(deepcopy(rootstate), action, self.id)
            
            heapq.heappush(queue, (f, index, next_state, action))  
            index += 1 

        while len(queue) and time.time() - start_time < THINKTIME:
            f, index, state, action = heapq.heappop(queue)  
        
            if f == 0 :
                print("f == 0",action)
                return action
            else:
                next_state = deepcopy(state)
                new_actions = self.GetActions(next_state)
                for new_action in new_actions:
                    g = self.calculate_g(new_action)
                    h = self.calculate_h(new_action)
                    f = g + h
                    next_state = self.game_rule.generateSuccessor(deepcopy(state), new_action, self.id)
                    heapq.heappush(queue, (f, index, next_state, new_action))
                    index += 1  

        best_action = heapq.heappop(queue)[3] # Choose a minimum f value for the action when the time is approaching 2s
        print("f != 0",best_action)
        return best_action
        








    
