import time, random
from Azul.azul_model import AzulGameRule as GameRule
from copy import deepcopy
from collections import deque
import Azul.azul_utils as utils

THINKTIME   = 0.9
NUM_PLAYERS = 2

# Defines this agent.
class myAgent():
    def __init__(self, _id):
        self.id = _id # Agent needs to remember its own id.
        self.game_rule = GameRule(NUM_PLAYERS)

    # Generates actions from this state.
    def GetActions(self, state):
        return self.game_rule.getLegalActions(state, self.id)
                    
    def DoAction(self, state, action):
        score = state.agents[self.id].score
        state = self.game_rule.generateSuccessor(state, action, self.id)

        if action[0] in (utils.Action.TAKE_FROM_FACTORY, utils.Action.TAKE_FROM_CENTRE):
            tile_grab = action[2]
            number_of_tiles = tile_grab.number
            pattern_line = tile_grab.pattern_line_dest
            # number_to_floor = tile_grab.num_to_floor_line
            agent_state = state.agents[self.id]
            wall_state = agent_state.grid_state[pattern_line]

            if any(tile == 1 for tile in wall_state):
                goal_reached = number_of_tiles == pattern_line + 1 
            else:
                goal_reached = number_of_tiles == pattern_line + 1
            return goal_reached


    def SelectAction(self, actions, rootstate):
        start_time = time.time()
        queue      = deque([ (deepcopy(rootstate),[]) ]) # Initialise queue. First node = root state and an empty path.
        
        # Conduct BFS starting from rootstate.
        while len(queue) and time.time()-start_time < THINKTIME:
            state, path = queue.popleft() # Pop the next node (state, path) in the queue.
            new_actions = self.GetActions(state) # Obtain new actions available to the agent in this state.
            
            for a in new_actions: # Then, for each of these actions...
                next_state = deepcopy(state)              # Copy the state.
                next_path  = path + [a]                   # Add this action to the path.
                goal     = self.DoAction(next_state, a) # Carry out this action on the state, and check for goal
                if goal:
                    print('path found:', next_path)
                    return next_path[0] # If the current action reached the goal, return the initial action that led there.
                else:
                    queue.append((next_state, next_path)) # Else, simply add this state and its path to the queue.
        
        return random.choice(actions) # If no goal was found in the time limit, return a random action.
        
    


# reference : # Author:  Steven Spratley
# Date:    04/01/2021
# Purpose: Implements an example breadth-first search agent for the COMP90054 competitive game environment.
