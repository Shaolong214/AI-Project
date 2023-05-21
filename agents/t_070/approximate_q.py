from Azul.azul_model import AzulGameRule as GameRule
import Azul.azul_utils as utils
import json
import os
import random
import copy
import numpy

NUM_PLAYERS = 2
GRID_SIZE = 5
FLOOR_SCORES = [-1,-1,-2,-2,-2,-3,-3]
ROW_BONUS = 2
COL_BONUS = 7
SET_BONUS = 10

class myAgent:

    def __init__(self, _id):
        self.id = _id 
        self.game_rule = GameRule(NUM_PLAYERS)

        self.alpha = 0.5  # learning rate
        self.discount = 0.9  # discount factor
        self.train_model = True
        self.epsilon = 1.0  # initial exploration rate
        self.epsilon_min = 0.01  # minimum exploration rate
        self.epsilon_decay = 0.995  # decay rate for exploration
        
        self.grid_state = numpy.zeros((GRID_SIZE,GRID_SIZE))

        self.weights_file = 'weights.json'
        self.weights = self.load_weights()  # Load weights 

        self.number_of = {}
        for tile in utils.Tile:
            self.number_of[tile] = 0

        if self.weights is None:
            self.weights = {}

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
        next_agent_state = next_game_state.agents[self.id]
        # Update local grid state and tile count
        self.grid_state = next_agent_state.grid_state
        self.number_of = next_agent_state.number_of

        def calculate_bonuses(state):
            completed_row = 0
            bonus_row = 0
            for i in range(GRID_SIZE):
                if all(state.grid_state[i][j] != 0 for j in range(GRID_SIZE)):
                    completed_row += 1
                    bonus_row = completed_row * ROW_BONUS

            bonus_col = 0
            completed_col = 0
            for i in range(GRID_SIZE):
                if all(state.grid_state[j][i] != 0 for j in range(GRID_SIZE)):
                    completed_col += 1
                    bonus_col = completed_col * COL_BONUS

            bonus_set = 0 
            completed_set = 0
            for tile in utils.Tile:
                if state.number_of[tile] == GRID_SIZE:
                    completed_set += 1
                    bonus_set = completed_set * SET_BONUS

            return bonus_row + bonus_col + bonus_set

        current_bonus = calculate_bonuses(current_agent_state)
        next_bonus = calculate_bonuses(next_agent_state)

        current_num_completed_pattern_line = sum(1 for i in range(current_agent_state.GRID_SIZE) 
                                                if current_agent_state.lines_number[i] == i + 1)
        
        next_num_completed_pattern_line = sum(1 for i in range(next_agent_state.GRID_SIZE) 
                                            if next_agent_state.lines_number[i] == i + 1)
        
        current_floor_tiles_score = sum(floor_score for floor_tile_exists, floor_score 
                                        in zip(game_state.agents[self.id].floor,
                                            game_state.agents[self.id].FLOOR_SCORES) if floor_tile_exists == 1)

        next_floor_tiles_score = sum(floor_score for floor_tile_exists, floor_score 
                                    in zip(next_game_state.agents[self.id].floor,
                                            next_game_state.agents[self.id].FLOOR_SCORES) if floor_tile_exists == 1)
    
        return {
            'complete_pattern_lines_added': next_num_completed_pattern_line - current_num_completed_pattern_line,
            'floor_score_change': next_floor_tiles_score - current_floor_tiles_score,
            'bonus_change': next_bonus - current_bonus}
    
    def get_q_value(self, state, action):
        """Calculate the Q-value for a given state and action."""

        # Extract the features from the current state-action pair
        features = self.extract_features(state, action)

        # Initialize the Q-value sum
        q_value = 0

        # For each feature, add the product of the feature's value and its corresponding weight to the sum
        for feature, f_value in features.items():
            if feature in self.weights:
                q_value += self.weights[feature] * f_value
        return q_value
    
    def SelectAction(self, actions, game_state):
        # If not in training mode, simply return the best action
        if not self.train_model:
            return self.best_action(game_state)
        else:
            # Use epsilon-greedy strategy to choose action
            
            random_number = random.random()

            if random_number < self.epsilon:
                # Explore: select a random action
                legal_actions = self.get_legal_actions(game_state)
                action = random.choice(legal_actions)
            else:
                # Exploit: select the best action based on current knowledge
                action = self.best_action(game_state)

            # Execute action and get the new state
            new_state = self.game_rule.generateSuccessor(copy.deepcopy(game_state), action, self.id)
            
            # Calculate reward for the action
            reward = self.calculate_reward(game_state, actions)

            # Update weight vector based on the action's reward
            self.update_weight_vector(game_state, action, new_state, reward)
            
            # Decay the epsilon after each action
            if self.epsilon > self.epsilon_min:
                self.epsilon *= self.epsilon_decay
            
            # Return the chosen action
            return action

    def update_weight_vector(self, state, action, next_state, reward):
        """Update the weight vector based on the given state and action."""

        # Load current weights
        self.weights = self.load_weights()

        # Get legal actions in the next state and their corresponding Q-values
        nextstep_actions = self.get_legal_actions(next_state)
        nextstep_q_values = [self.get_q_value(next_state, a) for a in nextstep_actions]

        # Find the maximum Q-value in the next step, defaulting to 0 if there are no actions
        max_q_next_step = max(nextstep_q_values, default=0)

        # Calculate the difference between the updated Q-value estimate and the old Q-value
        delta = reward + self.discount * max_q_next_step - self.get_q_value(state, action)

        # Extract the features from the current state-action pair
        features = self.extract_features(state, action)

        # Update the weight of each feature
        for feature_name, f_value in features.items():
            # If the feature hasn't been encountered before, its weight is assumed to be 0
            self.weights[feature_name] = self.weights.get(feature_name, 0) + self.alpha * delta * f_value

        # Save the updated weights
        self.save_weights()

        # Print the updated weights for debugging
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

        # Extract the features
        curr_features = self.extract_features(game_state, action)

        # Reward for each one of complete_pattern_lines_added that greater than 1 
        if curr_features['complete_pattern_lines_added'] > 1:
            reward += 1
        
        # Reward for each one of floor_score_change greater than 1 
        if curr_features['floor_score_change'] > 1:
            reward -= 1
        
        # Reward for each 'bonus_change' that greater than 1
        reward += curr_features['bonus_change']
        
        # If none of the conditions are met, assign a default reward
        if reward == 0:
            reward -= 0.1
        return reward 


       