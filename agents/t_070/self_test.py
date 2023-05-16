from Azul.azul_model import AzulGameRule as GameRule
from Azul.azul_model import AzulState 
import json
import os
import random
import copy
import Azul.azul_utils as utils
import numpy


NUM_PLAYERS = 2
GRID_SIZE = 5
grid_state = numpy.zeros((GRID_SIZE,GRID_SIZE))



            # Record of the number of tiles of each colour the agent
            # has placed in their grid (useful for end-game scoring)
number_of = {}
for tile in utils.Tile:
    number_of[tile] = 0

class myAgent:
    def __init__(self, _id):
        self.id = _id 
        self.game_rule = GameRule(NUM_PLAYERS)

        self.alpha = 0.5  # learning rate
        self.discount = 0.9  # discount factor
        self.train_model = True
        
        # save the weight after training one episode (one round of game), then load the weight use to train second 
        # episode (or in next round of game)
        self.weights = {}  # weight vector for every feature

        self.weights_file = 'weights.json'
        self.weights = self.load_weights()  # Load weights from file if available

    def save_weights(self):
        """Save the weights to a json file."""
        with open(self.weights_file, 'w') as f:
            json.dump(self.weights, f)

    def load_weights(self):
        """Load weights from the json file if it exists, else return an empty dictionary."""
        if os.path.exists(self.weights_file):
            with open(self.weights_file, 'r') as f:
                return json.load(f)
        else:
            return {}

    def get_legal_actions(self, state):
        """Get all legal actions for the state."""
        return self.game_rule.getLegalActions(state, self.id)

    def extract_features(self, game_state, action):
        """Extract useful features from the game state and action."""
        next_game_state = self.game_rule.generateSuccessor(copy.deepcopy(game_state), action, self.id)

        current_agent_state = game_state.agents[self.id]
        # lines_number store tiles number of each pattern line
        current_num_completed_pattern_line = sum(1 for i in range(current_agent_state.GRID_SIZE) 
                                                 if current_agent_state.lines_number[i] == i + 1)

        next_agent_state = next_game_state.agents[self.id]
        next_num_completed_pattern_line = sum(1 for i in range(next_agent_state.GRID_SIZE) 
                                              if next_agent_state.lines_number[i] == i + 1)
        # lost scores according to the number of tiles on floor
        current_floor_tiles_score = sum(floor_score for floor_tile_exists, floor_score 
                                        in zip(game_state.agents[self.id].floor,
                                               game_state.agents[self.id].FLOOR_SCORES) if floor_tile_exists == 1)

        next_floor_tiles_score = sum(floor_score for floor_tile_exists, floor_score 
                                     in zip(next_game_state.agents[self.id].floor,
                                            next_game_state.agents[self.id].FLOOR_SCORES) if floor_tile_exists == 1)
        # bonus 
        # cur_cols = current_agent_state.GetCompletedColumns()
        # cur_sets = current_agent_state.GetCompletedSets()
        # cur_rows = current_agent_state.GetCompletedRows()
        # current_bonus = (cur_cols * current_agent_state.COL_BONUS) + (cur_sets * current_agent_state.SET_BONUS) + (cur_rows * current_agent_state.ROW_BONUS)

        # next_cols = next_agent_state.GetCompletedColumns()
        # next_sets = next_agent_state.GetCompletedSets()
        # next_rows = next_agent_state.GetCompletedRows()
        # next_bonus = (next_cols * next_agent_state.COL_BONUS) + (next_sets * next_agent_state.SET_BONUS) + (next_rows * next_agent_state.ROW_BONUS)

        cur_cols = game_state.GetCompletedColumns()
        cur_sets = game_state.GetCompletedSets()
        cur_rows = game_state.GetCompletedRows()
        current_bonus = (cur_cols * game_state.COL_BONUS) + (cur_sets * game_state.SET_BONUS) + (cur_rows * game_state.ROW_BONUS)

        next_cols = next_game_state.GetCompletedColumns()
        next_sets = next_game_state.GetCompletedSets()
        next_rows = next_game_state.GetCompletedRows()
        next_bonus = (next_cols * next_game_state.COL_BONUS) + (next_sets * next_game_state.SET_BONUS) + (next_rows * next_game_state.ROW_BONUS)

        # the value of returned feature is f_value
        return {
            'complete_pattern_lines_added': next_num_completed_pattern_line - current_num_completed_pattern_line,
            'floor_score_change': next_floor_tiles_score - current_floor_tiles_score,
            'bonus_change': next_bonus - current_bonus
        }

    # def GetCompletedRows(game_state):
    #         completed = 0
    #         for i in range(GRID_SIZE):
    #             allin = True
    #             for j in range(GRID_SIZE):
    #                 if grid_state[i][j] == 0:
    #                     allin = False
    #                     break
    #             if allin:
    #                 completed += 1
    #         return completed

    #     # Compute number of completed columns in the agent's grid
    # def GetCompletedColumns(game_state):
    #         completed = 0
    #         for i in range(GRID_SIZE):
    #             allin = True
    #             for j in range(GRID_SIZE):
    #                 if grid_state[j][i] == 0:
    #                     allin = False
    #                     break
    #             if allin:
    #                 completed += 1
    #         return completed

    #     # Compute the number of completed tile sets in the agent's grid
    # def GetCompletedSets(game_state):
    #         completed = 0
    #         for tile in utils.Tile:
    #             if number_of[tile] == GRID_SIZE:
    #                 completed += 1
    #         return completed

    
    def get_q_value(self, state, action):
        """Calculate the Q value."""
        features = self.extract_features(state, action) # get features info of the a state by an action
        # initialise accumulative sum of the product between each weights and each features.
        return sum(self.weights.get(feature, 0) * f_value for feature, f_value in features.items())
    

    # def SelectAction(self, actions, game_state):
    #     if not self.train_model:
    #         return self.best_action(game_state)
        
    #     action = random.choice(self.get_legal_actions(game_state)) if random.random() < 0.1 else self.best_action(game_state)
        
    #     new_state = self.game_rule.generateSuccessor(copy.deepcopy(game_state), action, self.id)
    #     self.update_weight_vector(game_state, action, new_state, self.calculate_reward(self))
        
    #     return action

    def SelectAction(self, actions, game_state):
        # If not in training mode, simply return the best action
        if not self.train_model:
            return self.best_action(game_state)
        else:
            # Use epsilon-greedy strategy to choose action
            random_number = random.random()

            if random_number < 0.1:
                # Explore: select a random action
                legal_actions = self.get_legal_actions(game_state)
                action = random.choice(legal_actions)
            else:
                # Exploit: select the best action based on current knowledge
                action = self.best_action(game_state)

            # Execute action and get the new state
            new_state = self.game_rule.generateSuccessor(copy.deepcopy(game_state), action, self.id)

            # Calculate reward for the action
            reward = self.calculate_reward(self, game_state)

            # Update weight vector based on the action's reward
            self.update_weight_vector(game_state, action, new_state, reward)

            # Return the chosen action
            return action


    def update_weight_vector(self, state, action, next_state, reward):
        """Update the weight vector."""
        nextstep_actions = self.get_legal_actions(next_state)
        nextstep_q_values = [self.get_q_value(next_state, a) for a in nextstep_actions] #get q value for every states by each legal action
        max_q_next_step = max(nextstep_q_values, default=0)
        # Formula provided on lecture, get the new information of new state
        delta = reward + self.discount * max_q_next_step - self.get_q_value(state, action)
        # update weights of each feature value by a 'for' loop.
        features = self.extract_features(state, action)
        for feature_name, f_value in features.items():
            # assign 0 to weight if have not visited before
            self.weights[feature_name] = self.weights.get(feature_name, 0) + self.alpha * delta * f_value
        print(self.weights)

    def best_action(self, state):
        """Select the action with the maximum Q(s, a), if multiple, choose one at random."""
        legalActions = self.get_legal_actions(state)

        # Obtain the q value for all corresponding actions
        actions, q_values = zip(*((action, self.get_q_value(state, action)) for action in legalActions))

        # Obtain actions with the maximum qvalue (could be multiple)
        best_actions = [action for action, q_value in zip(actions, q_values) if q_value == max(q_values)]

        if not best_actions:
            return None

        return random.choice(best_actions)


    def calculate_reward(self, game_state, action): 
        """Calculate the reward based on the extracted features."""
        reward = 0        
        # current_agent_state = game_state.agents[self.id]

        # Extract the features
        curr_features = self.extract_features(self, game_state)

        # Reward for each one of complete_pattern_lines_added that greater than 1 
        if curr_features['complete_pattern_lines_added'] > 1:
            reward += 1
        
        # Reward for each one of floor_score_change greater than 1 
        if curr_features['floor_score_change'] > 1:
            reward -= 1
        
        # Reward for each 'bonus_change' that greater than 1
        if curr_features['bonus_change'] > 1:
            reward += 1
            
        return reward


    # def calculate_future_penalty(self, player_state):
    #     """Estimate the penalty in the future

    #     Args:
    #         player_state: Player state

    #     Returns:
    #         The estimation value
    #     """
    #     future_penalty = 0
    #     # Punish unfinished pattern line
    #     for i in range(1, 5):
    #         if player_state.lines_number[i] > 0:
    #             future_penalty += 1
    #     # Extra Punishment for fourth pattern line
    #     if player_state.lines_number[3] == 1:
    #         future_penalty += 1.5
    #     if player_state.lines_number[3] == 2:
    #         future_penalty += 0.5
    #     # Extra Punishment for fifth pattern line
    #     if player_state.lines_number[4] == 1:
    #         future_penalty += 2
    #     elif player_state.lines_number[4] == 2:
    #         future_penalty += 1
    #     return future_penalty

    # def calculate_future_bonus(self, game_state, player_id):
    #     """Estimate Future Bonus"""
    #     # TODO: provide a more accurate estimation
    #     future_bonus = 0
    #     player_state = game_state.agent[self.id]
    #     # Only consider cols and sets
    #     cols = player_state.GetCompletedColumns()
    #     sets = player_state.GetCompletedSets()
    #     rows = player_state.GetCompletedRows()
    #     bonus = (cols * player_state.COL_BONUS) + (sets * player_state.SET_BONUS) + (rows * player_state.ROW_BONUS)
    #     # It is ok to get the first player, however, since we can't get enough iteration, not consider this now.
    #     if game_state.next_first_player == player_id:
    #         future_bonus += 1
    #     future_bonus += bonus
    #     return future_bonus

    # def calculate_future_reward(self, game_state, player_id):
    #     """Use to calculate the reward of the future round

    #     Args:
    #         game_state: Current game state, the game state should be a end of a round
    #         player_id: The id of the player

    #     Returns:
    #         The estimation value
    #     """
    #     player_state = game_state.players[player_id]
                
    #     return self.calculate_future_bonus(game_state, player_id) - self.calculate_future_penalty(player_state)

