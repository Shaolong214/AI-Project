# IMPORTS AND CONSTANTS ----------------------------------------------------------------------------------------------#


import time, random
from Azul.azul_model import AzulGameRule as GameRule
from copy import deepcopy
from collections import deque

# New
from collections import defaultdict
from math import sqrt, log
from Azul.azul_model import AzulState

# from template import GameRule as GameRule2

THINKTIME   = 0.9
NUM_PLAYERS = 2


# FUNCTIONS ----------------------------------------------------------------------------------------------------------#

# Code below refering to:
# Week 9 Monte-Carlo Tree Search Notebook (
# [source code]: https://gibberblot.github.io/rl-notes/single-agent/mcts.html)

# Logic
# 1) Selection
# 2) Expansion
# 3) Simulation
# 4) Backpropagation

class nodes():

    visitTimes = defaultdict (lambda: 0) # initially, visit each node 0 times 

    def __init__(self, _id, parent, state, qfunction, bandit, reward = 0.0, action = None):
        self.id = _id 
        self.parent = parent
        self.state = state
        self.qfunction = qfunction
        self.game_rule = GameRule(NUM_PLAYERS) 
        self.bandit = bandit
        self.reward = reward
        self.action = action 
        self.children = []

    def get_value(self):
        pass

    def get_visits(self):
        return nodes.visitTimes[self.state]
    
    def roundOver(self):
        if self.state.TilesRemaining() == True:
            return True
        else:
            return False
        
    def gameOver(self):
        if self.game_rule.gameEnds() == True:
            return True
        else:
            return False
    
    def expandedFully(self):
        # Improve: Use set 
        pass
        
    def ucb1(self):
        pass

    def best_child(self, node):
        return 
    


class myAgent():

    def __init__(self, _id, mdp, qfunction, bandit):
        self.id = _id 
        self.game_rule = GameRule(NUM_PLAYERS) 
        self.agentState = AzulState.AgentState
        self.mdp = mdp
        self.qfunction = qfunction
        self.bandit = bandit

    def GetActions(self, state):
        return self.game_rule.getLegalActions(state, self.id)
    
    def checkGoal(self, state, action):
        pass 
            
    # MCTS -----------------------------------------------------------------------------
    def doSearch(self, actions, rootstate):
       
        start_time = time.time()
        
        while time.time()-start_time < THINKTIME:
       
            selectNode = self.selection(rootstate)
            child = self.expandsion(selectNode)
            reward = self.simulation(child)
            self.backpropagation(selectNode,child,reward)

            goal_reached = self.checkGoal(selectNode.state, selectNode.action)

        pass
    


    # Step 1:
    def selection(self, currentNode):
        # 1. Check if the terminal state ### --> run out of tiles & full filled row/col --> **gameOver()** 
        # --> check if len(legal action) == 0 
        # 2. Check if a root node is fully expand --> **expandedFully()**
        # 3. If a node is not fully expand --> expand it! --> **expandsion()**
        # --> all expand possible save to children list --> **children[]** --> includes Q(s,a)
        # 4. If a node is fully expand --> choose best child from children[] -->  **bestChild()**
        # --> Use **multi-armed bandit**  using Q(s,a) --> use code from QLearning 
        # Need: 1) gameOver() 2) expandedFully() 3) expandsion() 4) bestChild() 5) children[]
        
        # Only do selection if there is still tiles remaining
        while nodes.gameOver() == False and nodes.roundOver() == False:
            if nodes.expandedFully() == False:
                return self.expandsion(currentNode)
            else: 
                currentNode = self.bestChild(currentNode)
        return currentNode
            

    # Step 2:
    def expandsion(self):
        # 1. Check if the terminal state --> already done in selection()
        # 2. get all **legalActions()**
        # 3. use **random()** or **heurtisc()** choose a node to expand 
        # 4. assig reward to each state 
        pass

    # Step 3:
    def simulation():
        # 1. Check if the terminal state -->
        # 2. Get reward for each state --> choose the one with best reward
        pass

    # Step 4:
    def backpropagation(self, reward, child):
        pass
    



    
    
# END FILE -----------------------------------------------------------------------------------------------------------#