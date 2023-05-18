import copy
import random


self.children={}

def select(self,state, ):
        # If the current node is not fully expanded, return the node itself
        if not self.isFullyExpanded(state):
            return self

        # If the node is fully expanded, proceed to select from its children based on epsilon-greedy strategy
        else:
            actions = list(self.children.keys())
            qValues = [self.children[action].getValue() for action in actions]

            # Select an action randomly with 10% chance (exploration)
            if random.random() < 0.05:
                selected_action = random.choice(actions)
            # Otherwise select the action with the highest Q value (exploitation)
            else:
                max_q_value = max(qValues)
                best_actions = [action for action, q_value in zip(actions, qValues) if q_value == max_q_value]

                # If there are no best actions (when the game ends), return None
                if len(best_actions) == 0:
                    return None

                # Randomly select one of the best actions
                selected_action = random.choice(best_actions)

            # Get the child node corresponding to the selected action and recursively call select function on it
            child = self.children[selected_action]
            return child.select(child.state)


 