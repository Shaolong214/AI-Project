import heapq
import random
import Azul.azul_utils as utils
from Azul.azul_model import AzulGameRule as GameRule


NUM_PLAYERS = 2

    
class myAgent():
    def __init__(self, _id):
        self.id = _id # Agent needs to remember its own id.
        self.game_rule = GameRule(NUM_PLAYERS)

    def AstarSearch(self, game_state, agent_id):
        def heuristic(game_state):
            agent_state = game_state.agents[self.id]
            wall = agent_state.grid_scheme
            
            for i in range(agent_state.GRID_SIZE):
                grid_col = int(agent_state.grid_scheme[i][tile])
                agent_state.grid_state[i][grid_col] == 1

            total_cost = 0
            for row in range(agent_state.GRID_SIZE):
                for col in range(agent_state.GRID_SIZE):
                    if wall[row][col] == 1:
                        row_cost = abs(row - (agent_state.GRID_SIZE - 1) / 2)
                        col_cost = abs(col - (agent_state.GRID_SIZE - 1) / 2)
                        total_cost += row_cost + col_cost

            return total_cost



        def goal_state(game_state):
            # 1. think about the game rule itself
            # * current agent complete a row in the wall region (very slow)
            # * after executing some action, some pattern line is full (good) [for example]
                # how to detect that we can score at least one point (by completing a row in pattern line)?
                # -> more concrete: the agent can score at least point
                # step 1: figure out "when some score got added to a player"
                # finding: scoring for each player only happens when all factories and table center are empty
                # step 2: we need to implement some functions to calculate "instant score" before all factories and table center are empty

            if action[0] == utils.Action.TAKE_FROM_CENTRE or action[0] == utils.Action.TAKE_FROM_FACTORY:
                tile_grab = action[2]
                number_of_tiles = tile_grab.number
                if number_of_tiles == tile_grab.pattern_line_dest + 1 :

                    return True
            return False

        priority_queue = PriorityQueue()
        start_state = game_state
        start_node = (start_state, '', 0, [])
        priority_queue.push(start_node, heuristic(start_state))
        visited = set()
        best_g = dict()

        while not priority_queue.isEmpty():
            node = priority_queue.pop()
            state, action, cost, path = node
            if (not state in visited) or cost < best_g.get(state):
                visited.add(state)
                best_g[state] = cost
                if goal_state(state):
                    path = path + [action]
                    del path[0]
                    return path


                for action in self.game_rule.getLegalActions(state, agent_id):
                    succ = self.game_rule.generateSuccessor(state, action, agent_id)
                    


                    tmp_cost = 1
                    new_node = (succ, action, cost + tmp_cost, path + [action])
                    priority_queue.push(new_node, heuristic(succ) + cost + tmp_cost)

        return []

    def SelectAction(self, actions, game_state):
        res_actions = self.AstarSearch(game_state, self.id)
        if len(res_actions) == 0:
            return random.choice(actions)
        return res_actions[0]
    
class PriorityQueue:
    """
      Implements a priority queue data structure. Each inserted item
      has a priority associated with it and the client is usually interested
      in quick retrieval of the lowest-priority item in the queue. This
      data structure allows O(1) access to the lowest-priority item.
    """
    def __init__(self):
        self.heap = []
        self.count = 0

    def getMinimumPriority(self):
        return self.heap[0][0]

    def push(self, item, priority):
        entry = (priority, self.count, item)
        heapq.heappush(self.heap, entry)
        self.count += 1

    def pop(self):
        (_, _, item) = heapq.heappop(self.heap)
        return item

    def isEmpty(self):
        return len(self.heap) == 0