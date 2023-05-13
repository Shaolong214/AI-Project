from Azul.azul_model import AzulGameRule as GameRule
import json
import os
import random

NUM_PLAYERS = 2
class myAgent():
    def __init__(self, _id):
        self.id = _id 
        self.game_rule = GameRule(NUM_PLAYERS)

        self.alpha = 0.5  # learning rate
        self.discount = 0.9  # discount factor
        self.train_model = True

        self.weights = {}  # weight vector for every feature

        # save the weight after training one episode (one round of game), then load the weight use to train second 
        # episode (or in next round of game)
        self.weights_file = 'weights.json'
        # Load weights from file if available
        self.weights = self.load_weights()

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
            if current_agent_state.lines_number[i] == i + 1:  # lines_number store tiles number of each pattern line
                current_num_completed_pattern_line += 1

        # the number of completed pattern lines in the next state
        next_agent_state = next_game_state.agents[self.id]
        next_num_completed_pattern_line = 0
        for i in range(next_agent_state.GRID_SIZE):
            if next_agent_state.lines_number[i] == i + 1:
                next_num_completed_pattern_line += 1

        # lost scores due to the number of tiles on floor
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
        
        # Features returned by extract_features function defined by us
        # the value of returned feature is f_value
        return {
            'complete_pattern_lines_added': next_num_completed_pattern_line - current_num_completed_pattern_line,
            'floor_score_change': next_floor_tiles_score - current_floor_tiles_score 
        }

    def get_q_value(self, state, action):
        """Q(state, action)"""
        features = self.extract_features(state, action) # get features info of the a state by an action
        sum = 0 # initialise accumulative the sum of the product between each weights and each features.
        for feature, f_value in features.items(): 
            sum += self.weights.get(feature, 0) * f_value # for each feature has a correspond weight, initialse it as 0
        return sum

    def get_legal_actions(self, state):
        return self.game_rule.getLegalActions(state, self.id)

    def update_weight_vector(self, state, action, next_state, reward):
        ''' Calculate the maximum Q value first, then apply the formula '''
        nextstep_actions = self.get_legal_actions(next_state)
        nextstep_q_values = [self.get_q_value(next_state, a) for a in nextstep_actions] #get q value for every states by each legal action
        if len(nextstep_q_values) == 0:
            max_q_next_step = 0
        else:
            max_q_next_step = max(nextstep_q_values) # select the largest q value among all legal action
        # Formula provided on lecture, get the new information of new state
        delta = reward + self.discount * max_q_next_step - self.get_q_value(state, action)
        # update weights of each feature value by a for loop.
        features = self.extract_features(state, action)
        for feature_name, f_value in features.items():
            weight = self.weights.get(feature_name, 0)  # initial_weight = 0 if havn't seen before
            self.weights[feature_name] = weight + self.alpha * delta * f_value
        # print weights
        print(self.weights)

    def best_action(self, state):
        """select max Q(s, a), random pick if multiple"""
        legalActions = self.get_legal_actions(state)

        # get q value of every legal actions and store in two lists: actions and q_values
        actions = []
        q_values = []
        for a in legalActions:
            q_value = self.get_q_value(state, a)
            actions.append(a)
            q_values.append(q_value)

        # get best action of q value, there may have more than one best actions, if so, pick up randomly
        best_actions = []
        for i, q in enumerate(q_values):
            if q == max(q_values):
                best_actions.append(actions[i])

        if len(best_actions) == 0:
            return None
        # can be replace by a multi-armed bandits algorithm.
        return random.choice(best_actions)

    # train mode or not
    def SelectAction(self, actions, game_state):
        if not self.train_model:
            return self.best_action(game_state)
        else:
            # select action
            # implement epsilon - greedy: 0.1 probabilty return a random action, 0.9 probabilty return a best acion with max Q value.
            random_number = random.random()
            if random_number < 0.1:
                action = random.choice(self.get_legal_actions(game_state))
            else:
                action = self.best_action(game_state)
            # execute action
            new_state = self.game_rule.generateSuccessor(game_state, action, self.id)
            # TODO: calculate reward here based on old_state (game_state) and new_state
            reward = self.calculate_reward(game_state, new_state)

            # update weight vector, this the aim of training mode: upodate weight
            self.update_weight_vector(game_state, action, new_state, reward)

    def calculate_reward(self, old_state, new_state):
        return 1
