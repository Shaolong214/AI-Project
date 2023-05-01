# INFORMATION ------------------------------------------------------------------------------------------------------- #


# Author: 
# Date:    05/01/2023
# Purpose:


# IMPORTS AND CONSTANTS ----------------------------------------------------------------------------------------------#


import time, random
from Azul.azul_model import AzulGameRule as GameRule
from copy import deepcopy
from collections import deque

# New
from costRule import costH
from Azul.azul_model import AgentState
from collections import defaultdict
# from template import GameRule as GameRule2

THINKTIME   = 0.9
NUM_PLAYERS = 2


# FUNCTIONS ----------------------------------------------------------------------------------------------------------#

# Code below refering to:
# 1) Week 9 Monte-Carlo Tree Search Notebook (https://gibberblot.github.io/rl-notes/single-agent/mcts.html)
# 2) example_bfs.py file

# Logic
# 1) Selection
# 2) Expansion
# 3) Simulation
# 4) Backpropagation

class nodes():

    # Note: So far the code below is the same as the code in Week 9 Monte-Carlo Tree Search Notebook
    # begin-----------------------------------------------------------------------------------------
    visitTimes = defaultdict (lambda: 0) # initially, visit each node 0 times 

    def __init__(self, _id, mdp, parent, state:AgentState(), qfunction, bandit, reward = 0.0, action = None):
        self.id = _id 
        self.mdp = mdp
        self.parent = parent
        self.state = state
        self.qfunction = qfunction
        self.game_rule = GameRule(NUM_PLAYERS) 
        self.bandit = bandit
        self.reward = reward
        self.action = action 

    def get_visits(self):
        return myAgent.visitTimes[self.state]
    # end--------------------------------------------------------------------------------------------


class myAgent():

    #visitTimes = defaultdict (lambda: 0) # initially, visit each node 0 times 

    def __init__(self, _id, mdp, qfunction, bandit,agentState):
        self.id = _id 
        self.game_rule = GameRule(NUM_PLAYERS) 
        self.agentState = AgentState()
        self.mdp = mdp
        self.qfunction = qfunction
        self.bandit = bandit

    # Note: So far the code below is the same as the code in example_bfs.py file
    # begin-----------------------------------------------------------------------
    def GetActions(self, state):
        return self.game_rule.getLegalActions(state, self.id)
    
    def DoAction(self, state, action):
        score = state.agents[self.id].score
        state = self.game_rule.generateSuccessor(state, action, self.id)
        goal_reached = False #TODO: 
        return goal_reached
    # end---------------------------------------------------------------------------
    


    def doSearch(self, actions, rootstate):
        
        # Note: So far the code below is the same as the code in example_bfs.py file
        # begin-----------------------------------------------------------------------
        start_time = time.time()
        queue      = deque([ (deepcopy(rootstate),[]) ])
        while len(queue) and time.time()-start_time < THINKTIME:
        # end-------------------------------------------------------------------------
            pass


    def selection(self, rootstate):
        
        # Only do selection if there is still tiles remaining
        if self.agentState.TilesRemaining() == True:
            
            # Check if a node has expanded fully
            if  self.visitTimes:
                pass

    def expandsion():
        pass

    def simulation():
        pass

    def backpropagation():
        pass
    
        
    
# END FILE -----------------------------------------------------------------------------------------------------------#