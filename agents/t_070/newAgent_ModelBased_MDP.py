# IMPORTS AND CONSTANTS ----------------------------------------------------------------------------------------------#


import time, random
from Azul.azul_model import AzulGameRule as GameRule
from copy import deepcopy
from collections import deque
import Azul.azul_utils as utils
from Azul.azul_model import AzulState
import numpy as np
import copy

THINKTIME   = 0.9
NUM_PLAYERS = 2


# FUNCTIONS ----------------------------------------------------------------------------------------------------------#

# Reference: 
# Week 7 lecture notebook (https://gibberblot.github.io/rl-notes/single-agent/MDPs.html)
class MDPAgent():

    def __init__(self, _id):
        self.id = _id 
        self.game_rule = GameRule(NUM_PLAYERS) 
        self.agentState = AzulState.AgentState()

    def get_states(self, state, action):
        state = self.game_rule.generateSuccessor(state, action, self.id)
        #plr_state = state.agents[self.id]
        return state

    def get_actions(self,state):
        action = self.game_rule.getLegalActions(state, self.id)
        return action
    
    # I feel the transitions is mainly about 2 actions (pick from factory or center)
    # get_transitions[0] -- num_states
    # get_transitions[1] -- num_actions
    def get_transitions(self, state, action):
        transitions = []

        if action[0] == utils.Action.TAKE_FROM_FACTORY or action[0] == utils.Action.TAKE_FROM_CENTRE:
            stateCopy = copy.deepcopy(state)

            next_state = self.game_rule.generateSuccessor(stateCopy, action, self.id)
            agent_state = state.agents[self.id]

            tile_grab = action[2]
            number_of_tiles = tile_grab.number
            color_of_tiles = tile_grab.tile_type
            put_pattern_num = tile_grab.num_to_pattern_line
            patternLine_index = tile_grab.pattern_line_dest + 1
            factory_index = action[1] + 1
            put_foor_num = tile_grab.num_to_floor_line

            # [(state, action, probability)]
            prob = 1
            for i in range(1,6):
                s_new = next_state.lines_number[i] 
                s_old = agent_state.lines_number[i]
                leftOver = patternLine_index - s_old
            # P(s' = line 1 exist 1 | s = 1st line empty, a = pick up 1 tile) = 1
            # P(s' = line 2 exist 2 | s = 2nd line empty, a = pick up 2 same colored tiles) = 1
            # P(s' = line 3 exist 3 | s = 3rd line empty, a = pick up 3 same colored tiles) = 1
            # P(s' = line 4 exist 4 | s = 4th line empty, a = pick up 4 same colored tiles) = 1
            # P(s' = line 5 exist 5 | s = 5th line empty, a = pick up 5 same colored tiles) = 1
                if s_new == patternLine_index and s_old == 0 and number_of_tiles == patternLine_index:
                    transitionEle = s_new, s_old, action, prob  
                    transitions.append(transitionEle)
            # P(s' = line 2 exist 2 | s = 2nd line exist 1 tile, a = pick up 1 same colored tile) = 1
            # P(s' = line 3 exist 3 | s = 3rd line exist 1 tile, a = pick up 2 same colored tiles) = 1
            # P(s' = line 3 exist 3 | s = 3rd line exist 2 tile, a = pick up 1 same colored tiles) = 1
            # P(s' = line 4 exist 4 | s = 4th line exist 1 tile, a = pick up 3 same colored tile) = 1
            # P(s' = line 4 exist 4 | s = 4th line exist 2 tile, a = pick up 2 same colored tiles) = 1
            # P(s' = line 4 exist 4 | s = 4th line exist 3 tile, a = pick up 1 same colored tiles) = 1
            # P(s' = line 5 exist 4 | s = 5th line exist 1 tile, a = pick up 4 same colored tile) = 1
            # P(s' = line 5 exist 4 | s = 5th line exist 2 tile, a = pick up 3 same colored tiles) = 1
            # P(s' = line 5 exist 4 | s = 5th line exist 3 tile, a = pick up 2 same colored tiles) = 1
            # P(s' = line 5 exist 4 | s = 5th line exist 4 tile, a = pick up 1 same colored tiles) = 1
                elif s_new == patternLine_index and number_of_tiles == leftOver:
                    transitionEle = s_new, s_old, action, prob  
                    transitions.append(transitionEle)
            
            
                                                                                                                                                      



            # after take action: pick tiles from factory
            # it need to get all x number of y colored tile from factory z & put on ith line or floor or bag
            # E.g., "Agent 1 takes 1 yellow(Y) tiles from factory1 1Y placed in pattern line 1"
            # E.g., "Agent 1 takes 3 white(w) tiles from centre 2W placed in pattern line 3 1W placed in floor line"
            # E.g., "Agent 1 takes 4 yellow(Y) tiles from centre 4Y placed in floor line"
            # put 1 W on line 1 --> line 1 exist 1 W & put 2 B on line 2 etc 

            transitions.append()

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
        #return state

    # I feel the reward should consider all the situations
    # 1) complete a row/column/set 2) get closed tiles 3) deletion mark etc
    # The reward is calculated at the round end
    # However, I decide to start with a simple version
    # The reward will given once reach the goal
    def get_reward(self):
        #reward = self.agentState
        reward = 0
        if self.get_goal_states() == True:
            reward += 10
        else:
            reward = 0
        #reward = self.agentState.ScoreRound()
        return reward

    def is_terminal(self, state):
        if AzulState.TilesRemaining() == True:  # End of round: if run out of tiles
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
    # My goal is pick the number of tiles exact the same as the number put on the pattern line 
    def get_goal_states(self, state, action):
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
            
            # if not the 1st person pick up from center 
            if not state.first_agent_taken:
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


# Reference: 
# Week 7 lecture notebook (https://gibberblot.github.io/rl-notes/single-agent/value-iteration.html)
class valueIter():

    def __init__(self, _id):
        self.id = _id 
        self.mdp = MDPAgent()
        self.rewards = self.mdp.get_reward()
        self.transitions = self.mdp.get_transitions()
        self.num_states = len(self.transitions)
        self.num_actions = 4
        self.discount = self.mdp.get_discount_factor()
        self.values = np.zeros(self.num_states)
        self.policy = None

    #def bellmanEqu(self, state, action, new_state):
    #    prob = 1.0
    #    new_value = prob * (self.rewards[state] + self.discount * self.values.get_value(new_state)) 
    #    return new_value
    


    #def value_iteration(self, max_iterations = 100, theta = 0.001):
    #    for i in range(max_iterations):
    #        delta = 0.0
    #        new_values = 0
    #        for state in self.mdp.get_states():
    #            qtable = None
    #            for action in self.mdp.get_actions():
    #                new_value = 0.0
    #                for new_state in self.mdp.get_transitions(state, action):
    #                    new_value += self.bellmanEqu(self, state, action, new_state)
                         


# END FILE -----------------------------------------------------------------------------------------------------------#
