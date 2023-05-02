
import time, random
from Azul.azul_model import AzulGameRule as GameRule
from copy import deepcopy
from heapq import heappush, heappop

THINKTIME = 0.9
NUM_PLAYERS = 2


class myAgent():
    def init(self, _id):
        self.id = _id # Agent needs to remember its own id.
        self.game_rule = GameRule(NUM_PLAYERS) # Agent stores an instance of GameRule, from which to obtain functions.
# More advanced agents might find it useful to not be bound by the functions in GameRule, instead executing
# their own custom functions under GetActions and DoAction.

    # Generates actions from this state.
    def GetActions(self, state):
        return self.game_rule.getLegalActions(state, self.id)

    # Carry out a given action on this state and return True if goal is reached received.
    def DoAction(self, state, action):
        score = state.agents[self.id].score
        state = self.game_rule.generateSuccessor(state, action, self.id)

        goal_reached = False #TODO: Students, how should agent check whether it reached goal or not

        return goal_reached

    def heuristic(self, state):
        # TODO: Implement a heuristic function that estimates the cost from the current state to the goal
        return 0

    # Take a list of actions and an initial state, and perform A* search within a time limit.
    # Return the first action that leads to goal, if any was found.
    def SelectAction(self, actions, rootstate):
        start_time = time.time()
        open_list = [(0, deepcopy(rootstate), [])]  # Initialise priority queue. First node = root state and an empty path.

        # Conduct A* search starting from rootstate.
        while len(open_list) and time.time() - start_time < THINKTIME:
            _, state, path = heappop(open_list)  # Pop the next node (state, path) with the lowest cost in the priority queue.
            new_actions = self.GetActions(state)  # Obtain new actions available to the agent in this state.

            for a in new_actions:  # Then, for each of these actions...
                next_state = deepcopy(state)  # Copy the state.
                next_path = path + [a]  # Add this action to the path.
                goal = self.DoAction(next_state, a)  # Carry out this action on the state, and check for goal
                if goal:
                    print(f'Move {self.turn_count}, path found:', next_path)
                    return next_path[0]  # If the current action reached the goal, return the initial action that led there.
                else:
                    cost = len(next_path) + self.heuristic(next_state)
                    heappush(open_list, (cost, next_state, next_path))  # Else, simply add this state and its path to the queue with the calculated cost.

        return random.choice(actions)  # If no goal was found in the time limit, return a random action.
