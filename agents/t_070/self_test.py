from Azul.azul_model import AzulGameRule as GameRule
import json
import os
import random
import copy

NUM_PLAYERS = 2

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
        # the value of returned feature is f_value
        return {
            'complete_pattern_lines_added': next_num_completed_pattern_line - current_num_completed_pattern_line,
            'floor_score_change': next_floor_tiles_score - current_floor_tiles_score 
        }

    def get_q_value(self, state, action):
        """Calculate the Q value."""
        features = self.extract_features(state, action) # get features info of the a state by an action
        # initialise accumulative sum of the product between each weights and each features.
        return sum(self.weights.get(feature, 0) * f_value for feature, f_value in features.items())
    

    def SelectAction(self, actions, game_state):
        if not self.train_model:
            return self.best_action(game_state)
        
        action = random.choice(self.get_legal_actions(game_state)) if random.random() < 0.1 else self.best_action(game_state)
        
        new_state = self.game_rule.generateSuccessor(copy.deepcopy(game_state), action, self.id)
        self.update_weight_vector(game_state, action, new_state, self.calculate_reward(self))
        
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


    def calculate_reward(self, old_state):
        """Calculate the reward. This is a placeholder function and should be overridden with a problem-specific implementation."""
        return 1



       
