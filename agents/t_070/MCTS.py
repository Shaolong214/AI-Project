import time, random
from Azul.azul_model import AzulGameRule as GameRule
from copy import deepcopy
from math import sqrt, log


'''In this implementation, the Node class represents a node in the MCTS tree. The MCTS algorithm is implemented in 
the SelectAction function, which consists of the following steps:

Tree policy: Select a node to expand or simulate.
Expand the node, and add the resulting child node to the tree.
Simulate the action taken by the child node, and update the rewards and visits in the tree.
Backpropagate the results up the tree.
Return the best action found after the given amount of time.

The MCTS algorithm is more computationally expensive than BFS, but it can be more effective in finding better actions
in larger search spaces. '''




THINKTIME = 0.9
NUM_PLAYERS = 2
C = sqrt(2)

class Node:
    def __init__(self, state, parent=None, action=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.visits = 0
        self.reward = 0
        self.action = action

    def is_fully_expanded(self):
        return len(self.children) == len(self.state.getLegalActions(self.state.turn))

    def ucb1(self):
        return self.reward / self.visits + C * sqrt(log(self.parent.visits) / self.visits)


class myAgent():
    def __init__(self, _id):
        self.id = _id
        self.game_rule = GameRule(NUM_PLAYERS)

    def GetActions(self, state):
        return self.game_rule.getLegalActions(state, self.id)

    def DoAction(self, state, action):
        score = state.agents[self.id].score
        state = self.game_rule.generateSuccessor(state, action, self.id)

        goal_reached = False
        return goal_reached

    def SelectAction(self, actions, rootstate):
        start_time = time.time()

        root = Node(rootstate)

        while time.time() - start_time < THINKTIME:
            selected_node = self.tree_policy(root)
            goal_reached = self.DoAction(selected_node.state, selected_node.action)
            reward = 1 if goal_reached else 0
            self.backpropagate(selected_node, reward)

        best_child = self.best_child(root)
        return best_child.action

    def tree_policy(self, node):
        while not self.game_rule.isGameOver(node.state):
            if not node.is_fully_expanded():
                return self.expand(node)
            else:
                node = self.best_child(node)
        return node

    def expand(self, node):
        legal_actions = self.GetActions(node.state)
        untried_actions = [a for a in legal_actions if a not in [child.action for child in node.children]]

        action = random.choice(untried_actions)
        next_state = deepcopy(node.state)
        goal_reached = self.DoAction(next_state, action)

        child_node = Node(next_state, parent=node, action=action)
        node.children.append(child_node)

        return child_node

    def best_child(self, node, exploration_param=C):
        return max(node.children, key=lambda child: child.ucb1())

    def backpropagate(self, node, reward):
        while node is not None:
            node.visits += 1
            node.reward += reward
            node = node.parent
