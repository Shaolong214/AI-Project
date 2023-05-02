# Cost rule template
# The rule is used as a heuristic to decide which action should choose at each step.
# We would choose the action with the lowest cost
# - 1st rule: above row has higher priority than blow rows, (1st > 2nd > 3rd > 4th > 5th)
# Because the smaller the tiles number, the higher chance it moves to wall
# - 2nd rule: match the row number & tiles number (1 tile = 1st row number), o/w delete mark

# Note: (might relax the restrictions later)
# To simplify, first ignore the effects of prior & next action, 
# Each action only focus on itself and the current environment, without considering anyone else

# Logic:
# count the current number left over in each factor/center 
# Check the color of the tile
# Check which line is empty (e.g., 1st line/ 2nd line)
# If tile number > row number, delete mark

class costRule():

    def __init__(self, _id):
        pass
    
    def costH():
        pass