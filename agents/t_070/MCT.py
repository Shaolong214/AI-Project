
import time, random
from Azul.azul_model import AzulGameRule as GameRule
from copy import deepcopy
import Azul.azul_utils as utils

THINKTIME   = 0.8
NUM_PLAYERS = 2


class myMCTAgent():
    def __init__(self, _id):
        self.id = _id
        self.game_rule = GameRule(NUM_PLAYERS)
        self.root_state = None

    def GetActions(self, state):
        return self.game_rule.getLegalActions(state, self.id)
    
    def DoAction(self, state, action):
        score = state.agents[self.id].score
        state = self.game_rule.generateSuccessor(state, action, self.id)
        return state

    # Simulation function for MCTS
    def simulate(self, state):
        while not self.game_rule.gameEnds():
            actions = self.GetActions(state)
            action = random.choice(actions)
            state = self.DoAction(state, action)
        return self.game_rule.calScore(state, self.id)

    def SelectAction(self, actions, rootstate):
        start_time = time.time()
        simulations = 0

        # Initial root state
        if self.root_state is None:
            self.root_state = Node(None, rootstate, None)

        while time.time()-start_time < THINKTIME:
            simulations += 1
            node = self.root_state
            state = deepcopy(rootstate)

            # Selection
            while node.children:
                node = node.ucb1()
                state = self.DoAction(state, node.action)

            # Expansion
            if not self.game_rule.gameEnds():
                actions = self.GetActions(state)
                for action in actions:
                    node.add_child(action, self.DoAction(state, action))

            # Simulation
            while not self.game_rule.gameEnds():
                actions = self.GetActions(state)
                action = random.choice(actions)
                state = self.DoAction(state, action)

            # Backpropagation
            while node is not None:
                node.update(self.game_rule.calScore(state, self.id))
                node = node.parent

        return self.root_state.best_child().action


class Node:
    def __init__(self, action, state, parent):
        self.action = action
        self.state = state
        self.parent = parent
        self.children = []
        self.visits = 0
        self.wins = 0

    def add_child(self, action, state):
        child = Node(action, state, self)
        self.children.append(child)

    def update(self, result):
        self.visits += 1
        self.wins += result

    def ucb1(self):
        import math
        UCB1 = self.wins/self.visits + math.sqrt(2*math.log(self.parent.visits)/self.visits)
        return UCB1

    def best_child(self):
        sorted_children = sorted(self.children, key=lambda c: c.visits)
        return sorted_children[-1]