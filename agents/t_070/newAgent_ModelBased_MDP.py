# IMPORTS AND CONSTANTS ----------------------------------------------------------------------------------------------#


import time, random
from Azul.azul_model import AzulGameRule as GameRule
from copy import deepcopy
from collections import deque
import Azul.azul_utils as utils
from Azul.azul_model import AzulState
import numpy as np

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

        # I feel that I have checked my actions are legal action, thus, it would also be "valid_add" 
        #action = self.get_actions(state)
        #plr_state = state.agents[self.id]
        #plr_state.agent_trace.actions[-1].append(action)

        tile_grab = action[2]
        number_of_tiles = tile_grab.number
        color_of_tiles = tile_grab.tile_type
        #put_pattern_num = tile_grab.num_to_pattern_line
        patternLine_index = tile_grab.pattern_line_dest + 1
        factory_index = action[1] + 1
        #put_foor_num = tile_grab.num_to_floor_line

        if action == "ENDROUND":
            #state = self.get_states(state, action)
            #transitions += state
            pass

        elif action == "STARTROUND":
            # get_states() already provide all the necessary infromation for this state (e.g., number, color etc)
            #state = self.get_states(state, action)
            #transitions += state
            pass

        elif action[0] == utils.Action.TAKE_FROM_FACTORY:
            # after take action: pick tiles from factory
            # it need to get all x number of y colored tile from factory z & put on ith line or floor or bag
            # E.g., "Agent 1 takes 1 yellow(Y) tiles from factory1 1Y placed in pattern line 1"
            # E.f., "Agent 1 takes 3 white(w) tiles from centre 2W placed in pattern line 3 1W placed in floor line"
            # E.g., "Agent 1 takes 4 yellow(Y) tiles from centre 4Y placed in floor line"
            for factory_index in range(1,6): # For factory indexed 1,2,3,4,5
                
                if color_of_tiles == utils.Tile.RED:
                
                    if number_of_tiles == 1:
                
                        if patternLine_index == 1: 
                            each_element = [factory_index,'R', 1, 1, 1, 0] # factoryX, coloredX, num_TilesX, num_PatternX, pattern_indxX, num_FloorX
                            transitions.append(each_element)
                        elif patternLine_index == 2:
                            each_element = [factory_index,'R', 1, 1, 2, 0] # factoryX, coloredX, num_TilesX, num_PatternX, pattern_indxX, num_FloorX
                            transitions.append(each_element)
                        elif patternLine_index == 3:
                            each_element = [factory_index,'R', 1, 1, 3, 0] # factoryX, coloredX, num_TilesX, num_PatternX, pattern_indxX, num_FloorX
                            transitions.append(each_element)
                        elif patternLine_index == 4:
                            each_element = [factory_index,'R', 1, 1, 4, 0] # factoryX, coloredX, num_TilesX, num_PatternX, pattern_indxX, num_FloorX
                            transitions.append(each_element)
                        elif patternLine_index == 5:
                            each_element = [factory_index,'R', 1, 1, 5, 0] # factoryX, coloredX, num_TilesX, num_PatternX, pattern_indxX, num_FloorX
                            transitions.append(each_element)
                        
                    elif number_of_tiles == 2:
                        if patternLine_index == 1: 
                            each_element = [factory_index,'R', 2, 1, 1, 1] # factoryX, coloredX, num_TilesX, num_PatternX, pattern_indxX, num_FloorX
                            transitions.append(each_element)
                        elif patternLine_index == 2:
                            each_element = [factory_index,'R', 2, 2, 2, 0] # factoryX, coloredX, num_TilesX, num_PatternX, pattern_indxX, num_FloorX
                            transitions.append(each_element)
                        elif patternLine_index == 3:
                            each_element = [factory_index,'R', 2, 2, 3, 0] # factoryX, coloredX, num_TilesX, num_PatternX, pattern_indxX, num_FloorX
                            transitions.append(each_element)
                        elif patternLine_index == 4:
                            each_element = [factory_index,'R', 2, 2, 4, 0] # factoryX, coloredX, num_TilesX, num_PatternX, pattern_indxX, num_FloorX
                            transitions.append(each_element)
                        elif patternLine_index == 5:
                            each_element = [factory_index,'R', 2, 2, 5, 0] # factoryX, coloredX, num_TilesX, num_PatternX, pattern_indxX, num_FloorX
                            transitions.append(each_element)
            
                    elif number_of_tiles == 3:
                        if patternLine_index == 1: 
                            each_element = [factory_index,'R', 3, 1, 1, 2] # factoryX, coloredX, num_TilesX, num_PatternX, pattern_indxX, num_FloorX
                            transitions.append(each_element)
                        elif patternLine_index == 2:
                            each_element = [factory_index,'R', 3, 2, 2, 1] # factoryX, coloredX, num_TilesX, num_PatternX, pattern_indxX, num_FloorX
                            transitions.append(each_element)
                        elif patternLine_index == 3:
                            each_element = [factory_index,'R', 3, 3, 3, 0] # factoryX, coloredX, num_TilesX, num_PatternX, pattern_indxX, num_FloorX
                            transitions.append(each_element)
                        elif patternLine_index == 4:
                            each_element = [factory_index,'R', 3, 3, 4, 0] # factoryX, coloredX, num_TilesX, num_PatternX, pattern_indxX, num_FloorX
                            transitions.append(each_element)
                        elif patternLine_index == 5:
                            each_element = [factory_index,'R', 3, 3, 5, 0] # factoryX, coloredX, num_TilesX, num_PatternX, pattern_indxX, num_FloorX
                            transitions.append(each_element)
            

                    elif number_of_tiles == 4:
                        if patternLine_index == 1: 
                            each_element = [factory_index,'R', 4, 1, 1, 3] # factoryX, coloredX, num_TilesX, num_PatternX, pattern_indxX, num_FloorX
                            transitions.append(each_element)
                        elif patternLine_index == 2:
                            each_element = [factory_index,'R', 4, 2, 2, 2] # factoryX, coloredX, num_TilesX, num_PatternX, pattern_indxX, num_FloorX
                            transitions.append(each_element)
                        elif patternLine_index == 3:
                            each_element = [factory_index,'R', 4, 3, 3, 1] # factoryX, coloredX, num_TilesX, num_PatternX, pattern_indxX, num_FloorX
                            transitions.append(each_element)
                        elif patternLine_index == 4:
                            each_element = [factory_index,'R', 4, 4, 4, 0] # factoryX, coloredX, num_TilesX, num_PatternX, pattern_indxX, num_FloorX
                            transitions.append(each_element)
                        elif patternLine_index == 5:
                            each_element = [factory_index,'R', 4, 4, 5, 0] # factoryX, coloredX, num_TilesX, num_PatternX, pattern_indxX, num_FloorX
                            transitions.append(each_element)

                elif color_of_tiles == utils.Tile.BLUE:
                    if number_of_tiles == 1:
                        if patternLine_index == 1: 
                            each_element = [factory_index,'B', 1, 1, 1, 0] # factoryX, coloredX, num_TilesX, num_PatternX, pattern_indxX, num_FloorX
                            transitions.append(each_element)
                        elif patternLine_index == 2:
                            each_element = [factory_index,'B', 1, 1, 2, 0] # factoryX, coloredX, num_TilesX, num_PatternX, pattern_indxX, num_FloorX
                            transitions.append(each_element)
                        elif patternLine_index == 3:
                            each_element = [factory_index,'B', 1, 1, 3, 0] # factoryX, coloredX, num_TilesX, num_PatternX, pattern_indxX, num_FloorX
                            transitions.append(each_element)
                        elif patternLine_index == 4:
                            each_element = [factory_index,'B', 1, 1, 4, 0] # factoryX, coloredX, num_TilesX, num_PatternX, pattern_indxX, num_FloorX
                            transitions.append(each_element)
                        elif patternLine_index == 5:
                            each_element = [factory_index,'B', 1, 1, 5, 0] # factoryX, coloredX, num_TilesX, num_PatternX, pattern_indxX, num_FloorX
                            transitions.append(each_element)
                        
                    elif number_of_tiles == 2:
                        if patternLine_index == 1: 
                            each_element = [factory_index,'B', 2, 1, 1, 1] # factoryX, coloredX, num_TilesX, num_PatternX, pattern_indxX, num_FloorX
                            transitions.append(each_element)
                        elif patternLine_index == 2:
                            each_element = [factory_index,'B', 2, 2, 2, 0] # factoryX, coloredX, num_TilesX, num_PatternX, pattern_indxX, num_FloorX
                            transitions.append(each_element)
                        elif patternLine_index == 3:
                            each_element = [factory_index,'B', 2, 2, 3, 0] # factoryX, coloredX, num_TilesX, num_PatternX, pattern_indxX, num_FloorX
                            transitions.append(each_element)
                        elif patternLine_index == 4:
                            each_element = [factory_index,'B', 2, 2, 4, 0] # factoryX, coloredX, num_TilesX, num_PatternX, pattern_indxX, num_FloorX
                            transitions.append(each_element)
                        elif patternLine_index == 5:
                            each_element = [factory_index,'B', 2, 2, 5, 0] # factoryX, coloredX, num_TilesX, num_PatternX, pattern_indxX, num_FloorX
                            transitions.append(each_element)
            
                    elif number_of_tiles == 3:
                        if patternLine_index == 1: 
                            each_element = [factory_index,'B', 3, 1, 1, 2] # factoryX, coloredX, num_TilesX, num_PatternX, pattern_indxX, num_FloorX
                            transitions.append(each_element)
                        elif patternLine_index == 2:
                            each_element = [factory_index,'B', 3, 2, 2, 1] # factoryX, coloredX, num_TilesX, num_PatternX, pattern_indxX, num_FloorX
                            transitions.append(each_element)
                        elif patternLine_index == 3:
                            each_element = [factory_index,'B', 3, 3, 3, 0] # factoryX, coloredX, num_TilesX, num_PatternX, pattern_indxX, num_FloorX
                            transitions.append(each_element)
                        elif patternLine_index == 4:
                            each_element = [factory_index,'B', 3, 3, 4, 0] # factoryX, coloredX, num_TilesX, num_PatternX, pattern_indxX, num_FloorX
                            transitions.append(each_element)
                        elif patternLine_index == 5:
                            each_element = [factory_index,'B', 3, 3, 5, 0] # factoryX, coloredX, num_TilesX, num_PatternX, pattern_indxX, num_FloorX
                            transitions.append(each_element)

                    elif number_of_tiles == 4:
                        if patternLine_index == 1: 
                            each_element = [factory_index,'B', 4, 1, 1, 3] # factoryX, coloredX, num_TilesX, num_PatternX, pattern_indxX, num_FloorX
                            transitions.append(each_element)
                        elif patternLine_index == 2:
                            each_element = [factory_index,'B', 4, 2, 2, 2] # factoryX, coloredX, num_TilesX, num_PatternX, pattern_indxX, num_FloorX
                            transitions.append(each_element)
                        elif patternLine_index == 3:
                            each_element = [factory_index,'B', 4, 3, 3, 1] # factoryX, coloredX, num_TilesX, num_PatternX, pattern_indxX, num_FloorX
                            transitions.append(each_element)
                        elif patternLine_index == 4:
                            each_element = [factory_index,'B', 4, 4, 4, 0] # factoryX, coloredX, num_TilesX, num_PatternX, pattern_indxX, num_FloorX
                            transitions.append(each_element)
                        elif patternLine_index == 5:
                            each_element = [factory_index,'B', 4, 4, 5, 0] # factoryX, coloredX, num_TilesX, num_PatternX, pattern_indxX, num_FloorX
                            transitions.append(each_element)

                elif color_of_tiles == utils.Tile.WHITE:
                    if number_of_tiles == 1:
                        if patternLine_index == 1: 
                            each_element = [factory_index,'W', 1, 1, 1, 0] # factoryX, coloredX, num_TilesX, num_PatternX, pattern_indxX, num_FloorX
                            transitions.append(each_element)
                        elif patternLine_index == 2:
                            each_element = [factory_index,'W', 1, 1, 2, 0] # factoryX, coloredX, num_TilesX, num_PatternX, pattern_indxX, num_FloorX
                            transitions.append(each_element)
                        elif patternLine_index == 3:
                            each_element = [factory_index,'W', 1, 1, 3, 0] # factoryX, coloredX, num_TilesX, num_PatternX, pattern_indxX, num_FloorX
                            transitions.append(each_element)
                        elif patternLine_index == 4:
                            each_element = [factory_index,'W', 1, 1, 4, 0] # factoryX, coloredX, num_TilesX, num_PatternX, pattern_indxX, num_FloorX
                            transitions.append(each_element)
                        elif patternLine_index == 5:
                            each_element = [factory_index,'W', 1, 1, 5, 0] # factoryX, coloredX, num_TilesX, num_PatternX, pattern_indxX, num_FloorX
                            transitions.append(each_element)
                        
                    elif number_of_tiles == 2:
                        if patternLine_index == 1: 
                            each_element = [factory_index,'W', 2, 1, 1, 1] # factoryX, coloredX, num_TilesX, num_PatternX, pattern_indxX, num_FloorX
                            transitions.append(each_element)
                        elif patternLine_index == 2:
                            each_element = [factory_index,'W', 2, 2, 2, 0] # factoryX, coloredX, num_TilesX, num_PatternX, pattern_indxX, num_FloorX
                            transitions.append(each_element)
                        elif patternLine_index == 3:
                            each_element = [factory_index,'W', 2, 2, 3, 0] # factoryX, coloredX, num_TilesX, num_PatternX, pattern_indxX, num_FloorX
                            transitions.append(each_element)
                        elif patternLine_index == 4:
                            each_element = [factory_index,'W', 2, 2, 4, 0] # factoryX, coloredX, num_TilesX, num_PatternX, pattern_indxX, num_FloorX
                            transitions.append(each_element)
                        elif patternLine_index == 5:
                            each_element = [factory_index,'W', 2, 2, 5, 0] # factoryX, coloredX, num_TilesX, num_PatternX, pattern_indxX, num_FloorX
                            transitions.append(each_element)
            
                        if patternLine_index == 1: 
                            each_element = [factory_index,'W', 3, 1, 1, 2] # factoryX, coloredX, num_TilesX, num_PatternX, pattern_indxX, num_FloorX
                            transitions.append(each_element)
                        elif patternLine_index == 2:
                            each_element = [factory_index,'W', 3, 2, 2, 1] # factoryX, coloredX, num_TilesX, num_PatternX, pattern_indxX, num_FloorX
                            transitions.append(each_element)
                        elif patternLine_index == 3:
                            each_element = [factory_index,'W', 3, 3, 3, 0] # factoryX, coloredX, num_TilesX, num_PatternX, pattern_indxX, num_FloorX
                            transitions.append(each_element)
                        elif patternLine_index == 4:
                            each_element = [factory_index,'W', 3, 3, 4, 0] # factoryX, coloredX, num_TilesX, num_PatternX, pattern_indxX, num_FloorX
                            transitions.append(each_element)
                        elif patternLine_index == 5:
                            each_element = [factory_index,'W', 3, 3, 5, 0] # factoryX, coloredX, num_TilesX, num_PatternX, pattern_indxX, num_FloorX
                            transitions.append(each_element)

                    elif number_of_tiles == 4:
                        if patternLine_index == 1: 
                            each_element = [factory_index,'W', 4, 1, 1, 3] # factoryX, coloredX, num_TilesX, num_PatternX, pattern_indxX, num_FloorX
                            transitions.append(each_element)
                        elif patternLine_index == 2:
                            each_element = [factory_index,'W', 4, 2, 2, 2] # factoryX, coloredX, num_TilesX, num_PatternX, pattern_indxX, num_FloorX
                            transitions.append(each_element)
                        elif patternLine_index == 3:
                            each_element = [factory_index,'W', 4, 3, 3, 1] # factoryX, coloredX, num_TilesX, num_PatternX, pattern_indxX, num_FloorX
                            transitions.append(each_element)
                        elif patternLine_index == 4:
                            each_element = [factory_index,'W', 4, 4, 4, 0] # factoryX, coloredX, num_TilesX, num_PatternX, pattern_indxX, num_FloorX
                            transitions.append(each_element)
                        elif patternLine_index == 5:
                            each_element = [factory_index,'W', 4, 4, 5, 0] # factoryX, coloredX, num_TilesX, num_PatternX, pattern_indxX, num_FloorX
                            transitions.append(each_element)

                elif color_of_tiles == utils.Tile.BLACK:
                    if number_of_tiles == 1:
                        if patternLine_index == 1: 
                            each_element = [factory_index,'K', 1, 1, 1, 0] # factoryX, coloredX, num_TilesX, num_PatternX, pattern_indxX, num_FloorX
                            transitions.append(each_element)
                        elif patternLine_index == 2:
                            each_element = [factory_index,'K', 1, 1, 2, 0] # factoryX, coloredX, num_TilesX, num_PatternX, pattern_indxX, num_FloorX
                            transitions.append(each_element)
                        elif patternLine_index == 3:
                            each_element = [factory_index,'K', 1, 1, 3, 0] # factoryX, coloredX, num_TilesX, num_PatternX, pattern_indxX, num_FloorX
                            transitions.append(each_element)
                        elif patternLine_index == 4:
                            each_element = [factory_index,'K', 1, 1, 4, 0] # factoryX, coloredX, num_TilesX, num_PatternX, pattern_indxX, num_FloorX
                            transitions.append(each_element)
                        elif patternLine_index == 5:
                            each_element = [factory_index,'K', 1, 1, 5, 0] # factoryX, coloredX, num_TilesX, num_PatternX, pattern_indxX, num_FloorX
                            transitions.append(each_element)
                        
                    elif number_of_tiles == 2:
                        if patternLine_index == 1: 
                            each_element = [factory_index,'K', 2, 1, 1, 1] # factoryX, coloredX, num_TilesX, num_PatternX, pattern_indxX, num_FloorX
                            transitions.append(each_element)
                        elif patternLine_index == 2:
                            each_element = [factory_index,'K', 2, 2, 2, 0] # factoryX, coloredX, num_TilesX, num_PatternX, pattern_indxX, num_FloorX
                            transitions.append(each_element)
                        elif patternLine_index == 3:
                            each_element = [factory_index,'K', 2, 2, 3, 0] # factoryX, coloredX, num_TilesX, num_PatternX, pattern_indxX, num_FloorX
                            transitions.append(each_element)
                        elif patternLine_index == 4:
                            each_element = [factory_index,'K', 2, 2, 4, 0] # factoryX, coloredX, num_TilesX, num_PatternX, pattern_indxX, num_FloorX
                            transitions.append(each_element)
                        elif patternLine_index == 5:
                            each_element = [factory_index,'K', 2, 2, 5, 0] # factoryX, coloredX, num_TilesX, num_PatternX, pattern_indxX, num_FloorX
                            transitions.append(each_element)
            
                    elif number_of_tiles == 3:
                        if patternLine_index == 1: 
                            each_element = [factory_index,'K', 3, 1, 1, 2] # factoryX, coloredX, num_TilesX, num_PatternX, pattern_indxX, num_FloorX
                            transitions.append(each_element)
                        elif patternLine_index == 2:
                            each_element = [factory_index,'K', 3, 2, 2, 1] # factoryX, coloredX, num_TilesX, num_PatternX, pattern_indxX, num_FloorX
                            transitions.append(each_element)
                        elif patternLine_index == 3:
                            each_element = [factory_index,'K', 3, 3, 3, 0] # factoryX, coloredX, num_TilesX, num_PatternX, pattern_indxX, num_FloorX
                            transitions.append(each_element)
                        elif patternLine_index == 4:
                            each_element = [factory_index,'K', 3, 3, 4, 0] # factoryX, coloredX, num_TilesX, num_PatternX, pattern_indxX, num_FloorX
                            transitions.append(each_element)
                        elif patternLine_index == 5:
                            each_element = [factory_index,'K', 3, 3, 5, 0] # factoryX, coloredX, num_TilesX, num_PatternX, pattern_indxX, num_FloorX
                            transitions.append(each_element)

                    elif number_of_tiles == 4:
                        if patternLine_index == 1: 
                            each_element = [factory_index,'K', 4, 1, 1, 3] # factoryX, coloredX, num_TilesX, num_PatternX, pattern_indxX, num_FloorX
                            transitions.append(each_element)
                        elif patternLine_index == 2:
                            each_element = [factory_index,'K', 4, 2, 2, 2] # factoryX, coloredX, num_TilesX, num_PatternX, pattern_indxX, num_FloorX
                            transitions.append(each_element)
                        elif patternLine_index == 3:
                            each_element = [factory_index,'K', 4, 3, 3, 1] # factoryX, coloredX, num_TilesX, num_PatternX, pattern_indxX, num_FloorX
                            transitions.append(each_element)
                        elif patternLine_index == 4:
                            each_element = [factory_index,'K', 4, 4, 4, 0] # factoryX, coloredX, num_TilesX, num_PatternX, pattern_indxX, num_FloorX
                            transitions.append(each_element)
                        elif patternLine_index == 5:
                            each_element = [factory_index,'K', 4, 4, 5, 0] # factoryX, coloredX, num_TilesX, num_PatternX, pattern_indxX, num_FloorX
                            transitions.append(each_element)

                elif color_of_tiles == utils.Tile.YELLOW:
                    if number_of_tiles == 1:
                        if patternLine_index == 1: 
                            each_element = [factory_index,'Y', 1, 1, 1, 0] # factoryX, coloredX, num_TilesX, num_PatternX, pattern_indxX, num_FloorX
                            transitions.append(each_element)
                        elif patternLine_index == 2:
                            each_element = [factory_index,'Y', 1, 1, 2, 0] # factoryX, coloredX, num_TilesX, num_PatternX, pattern_indxX, num_FloorX
                            transitions.append(each_element)
                        elif patternLine_index == 3:
                            each_element = [factory_index,'Y', 1, 1, 3, 0] # factoryX, coloredX, num_TilesX, num_PatternX, pattern_indxX, num_FloorX
                            transitions.append(each_element)
                        elif patternLine_index == 4:
                            each_element = [factory_index,'Y', 1, 1, 4, 0] # factoryX, coloredX, num_TilesX, num_PatternX, pattern_indxX, num_FloorX
                            transitions.append(each_element)
                        elif patternLine_index == 5:
                            each_element = [factory_index,'Y', 1, 1, 5, 0] # factoryX, coloredX, num_TilesX, num_PatternX, pattern_indxX, num_FloorX
                            transitions.append(each_element)
                        
                    elif number_of_tiles == 2:
                        if patternLine_index == 1: 
                            each_element = [factory_index,'Y', 2, 1, 1, 1] # factoryX, coloredX, num_TilesX, num_PatternX, pattern_indxX, num_FloorX
                            transitions.append(each_element)
                        elif patternLine_index == 2:
                            each_element = [factory_index,'Y', 2, 2, 2, 0] # factoryX, coloredX, num_TilesX, num_PatternX, pattern_indxX, num_FloorX
                            transitions.append(each_element)
                        elif patternLine_index == 3:
                            each_element = [factory_index,'Y', 2, 2, 3, 0] # factoryX, coloredX, num_TilesX, num_PatternX, pattern_indxX, num_FloorX
                            transitions.append(each_element)
                        elif patternLine_index == 4:
                            each_element = [factory_index,'Y', 2, 2, 4, 0] # factoryX, coloredX, num_TilesX, num_PatternX, pattern_indxX, num_FloorX
                            transitions.append(each_element)
                        elif patternLine_index == 5:
                            each_element = [factory_index,'Y', 2, 2, 5, 0] # factoryX, coloredX, num_TilesX, num_PatternX, pattern_indxX, num_FloorX
                            transitions.append(each_element)
            
                    elif number_of_tiles == 3:
                        if patternLine_index == 1: 
                            each_element = [factory_index,'Y', 3, 1, 1, 2] # factoryX, coloredX, num_TilesX, num_PatternX, pattern_indxX, num_FloorX
                            transitions.append(each_element)
                        elif patternLine_index == 2:
                            each_element = [factory_index,'Y', 3, 2, 2, 1] # factoryX, coloredX, num_TilesX, num_PatternX, pattern_indxX, num_FloorX
                            transitions.append(each_element)
                        elif patternLine_index == 3:
                            each_element = [factory_index,'Y', 3, 3, 3, 0] # factoryX, coloredX, num_TilesX, num_PatternX, pattern_indxX, num_FloorX
                            transitions.append(each_element)
                        elif patternLine_index == 4:
                            each_element = [factory_index,'Y', 3, 3, 4, 0] # factoryX, coloredX, num_TilesX, num_PatternX, pattern_indxX, num_FloorX
                            transitions.append(each_element)
                        elif patternLine_index == 5:
                            each_element = [factory_index,'Y', 3, 3, 5, 0] # factoryX, coloredX, num_TilesX, num_PatternX, pattern_indxX, num_FloorX
                            transitions.append(each_element)

                    elif number_of_tiles == 4:
                        if patternLine_index == 1: 
                            each_element = [factory_index,'Y', 4, 1, 1, 3] # factoryX, coloredX, num_TilesX, num_PatternX, pattern_indxX, num_FloorX
                            transitions.append(each_element)
                        elif patternLine_index == 2:
                            each_element = [factory_index,'Y', 4, 2, 2, 2] # factoryX, coloredX, num_TilesX, num_PatternX, pattern_indxX, num_FloorX
                            transitions.append(each_element)
                        elif patternLine_index == 3:
                            each_element = [factory_index,'Y', 4, 3, 3, 1] # factoryX, coloredX, num_TilesX, num_PatternX, pattern_indxX, num_FloorX
                            transitions.append(each_element)
                        elif patternLine_index == 4:
                            each_element = [factory_index,'Y', 4, 4, 4, 0] # factoryX, coloredX, num_TilesX, num_PatternX, pattern_indxX, num_FloorX
                            transitions.append(each_element)
                        elif patternLine_index == 5:
                            each_element = [factory_index,'Y', 4, 4, 5, 0] # factoryX, coloredX, num_TilesX, num_PatternX, pattern_indxX, num_FloorX
                            transitions.append(each_element)

        elif action[0] == utils.Action.TAKE_FROM_CENTRE:
            pass

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
    def get_goal_states(self, state):
        #if self.agentState.GetCompletedRows() or  self.agentState.GetCompletedColumns() or self.agentState.GetCompletedSets():
        #    return True
        action =  self.game_rule.getLegalActions(state, self.id)
        tile_grab = action[2]
        number_of_tiles = tile_grab.number
        #color_of_tiles = tile_grab.tile_type
        put_pattern_num = tile_grab.num_to_pattern_line
        #patternLine_index = tile_grab.pattern_line_dest + 1
        #factory_index = action[1] + 1
        
        if number_of_tiles == put_pattern_num:
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
