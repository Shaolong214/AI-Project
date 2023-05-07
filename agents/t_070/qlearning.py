import random

from Azul.azul_model import AzulGameRule as GameRule

import json
import os
NUM_PLAYERS = 2
class myAgent():
    def __init__(self, _id):
        self.id = _id # Agent needs to remember its own id.
        self.game_rule = GameRule(NUM_PLAYERS)

        self.alpha = 0.5  # learning rate
        self.discount = 0.8  # discount factor

        self.train_model = True

        # self.weights = {}  # weight vector for every feature

        # # TODO: after training for one episode (a complete game), we need to save the weights on disk
        # # TODO: in next episode, we read the starting point of self.weights from disk
        # self.weights_file = 'weights.json'
        # # Load weights from file if available
        # self.weights = self.load_weights()

    def save_weights(self):
        with open(self.weights_file, 'w') as f:
            json.dump(self.weights, f)

    def load_weights(self):
        if os.path.exists(self.weights_file):
            with open(self.weights_file, 'r') as f:
                return json.load(f)
        else:
            return {}  # Return an empty dictionary if the file does not exist
        

    def extract_features(self, game_state, action):
        next_game_state = self.game_rule.generateSuccessor(game_state, action, self.id)

        # the number of completed pattern lines in the current state
        current_agent_state = game_state.agents[self.id]
        current_num_completed_pattern_line = 0
        for i in range(current_agent_state.GRID_SIZE):
            if current_agent_state.lines_number[i] == i + 1:
                current_num_completed_pattern_line += 1

        # the number of completed pattern lines in the next state
        next_agent_state = next_game_state.agents[self.id]
        next_num_completed_pattern_line = 0
        for i in range(next_agent_state.GRID_SIZE):
            if next_agent_state.lines_number[i] == i + 1:
                next_num_completed_pattern_line += 1

        # the score of the floor line in the current state
        current_floor_tiles_score = 0
        for floor_tile_exists, floor_score in zip(game_state.agents[self.id].floor,
                                                  game_state.agents[self.id].FLOOR_SCORES):
            if floor_tile_exists == 1:
                current_floor_tiles_score += floor_score

        # the score of the floor line in next state
        next_floor_tiles_score = 0
        for floor_tile_exists, floor_score in zip(next_game_state.agents[self.id].floor,
                                                  next_game_state.agents[self.id].FLOOR_SCORES):
            if floor_tile_exists == 1:
                next_floor_tiles_score += floor_score

        # TODO: add more features here

        return {
            'complete_pattern_lines_added': next_num_completed_pattern_line - current_num_completed_pattern_line,
            'floor_score_change': next_floor_tiles_score - current_floor_tiles_score
        }

    def get_q_value(self, state, action):
        """Q(state, action)"""
        features = self.extract_features(state, action)
        sum = 0
        for feature, f_value in features.items():
            sum += self.weights.get(feature, 0) * f_value
        return sum

    def get_legal_actions(self, state):
        return self.game_rule.getLegalActions(state, self.id)

    def update_weight_vector(self, state, action, next_state, reward):
        nextstep_actions = self.get_legal_actions(next_state)
        nextstep_q_values = [self.get_q_value(next_state, a) for a in nextstep_actions]
        if len(nextstep_q_values) == 0:
            max_q_next_step = 0
        else:
            max_q_next_step = max(nextstep_q_values)

        difference = reward + self.discount * max_q_next_step - self.get_q_value(state, action)
        features = self.extract_features(state, action)
        for feature_name, f_value in features.items():
            weight = self.weights.get(feature_name, 0)  # initial_weight = 0 if havn't seen before
            self.weights[feature_name] = weight + self.alpha * difference * f_value
        # print weights
        print(self.weights)

    def best_action(self, state):
        """select max Q(s, a), random pick if multiple"""
        legalActions = self.get_legal_actions(state)

        # get q value of its corresponding action 
        actions = []
        q_values = []
        for a in legalActions:
            q_value = self.get_q_value(state, a)
            actions.append(a)
            q_values.append(q_value)

        # get best action of q value (one or more)
        best_actions = []
        for i, q in enumerate(q_values):
            if q == max(q_values):
                best_actions.append(actions[i])

        if len(best_actions) == 0:
            return None

        return random.choice(best_actions)

    def SelectAction(self, actions, game_state):
        if not self.train_model:
            return self.best_action(game_state)
        else:
            # select action
            # implement epsilon - greedy
            random_number = random.random()
            if random_number < 0.1:
                action = random.choice(self.get_legal_actions(game_state))
            else:
                action = self.best_action(game_state)
            # execute action
            new_state = self.game_rule.generateSuccessor(game_state, action, self.id)
            # TODO: calculate some reward here
            # TODO: based on old_state (game_state) and new_state

            reward = self.calculate_reward(game_state, new_state)

            # update weight vector
            self.update_weight_vector(game_state, action, new_state, reward)

    def calculate_reward(self, old_state, new_state):
    # Reward function based on the difference in scores between old_state and new_state
        old_score = old_state.agents[self.id].score
        new_score = new_state.agents[self.id].score

        return new_score - old_score
