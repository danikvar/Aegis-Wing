"""
The agent superclass.
This class defines shared methods between all agents.
"""
from Movements import Movements

class Agent:
    def __init__(self, agent_length=1, agent_height=1, lowest_row=0, least_col=0):
        if agent_length < 1:
            raise ValueError("Agent size length must be >= 1")
        if agent_height < 1:
            raise ValueError("Agent size height must be >= 1")

        if lowest_row < 0:
            raise ValueError('Agent cannot start at any x position less than 0, (leftmost limit)')
        if least_col < 0:
            raise ValueError('Agent cannot start at any y position less than 0 (bottom limit)')

        # possible case where enemies start at edge of board or even behind it?

        self.agent_length = agent_length
        self.agent_height = agent_height
        # position of least left
        self.lowest_row = lowest_row
        # position of lowest side
        self.least_col = least_col

    def get_position(self) -> tuple:
        '''
        Returns a tuple representing lowest left x position
        and lowest y position
        :return: {tuple} (furthest left x post, highest y pos)
        '''
        return (self.lowest_row, self.least_col)

    def get_agent_size(self) -> tuple:
        return (self.agent_length, self.agent_height)


    def get_min_col_boundary(self):
        return self.least_col

    def get_max_col_boundary(self):
        if self.agent_length == 1:
            return self.least_col
        else:
            # i.e. if pos_x = 2
            # and agent_len_x = 3
            # spaced taken up is x = 2,3,4
            # 2 + 3 = 5, 5 is empty space
            return self.least_col + self.agent_length - 1

    def get_col_boundaries(self) -> tuple:
        return (self.least_col, self.get_max_col_boundary())

    def get_min_row_boundary(self) -> int:
        return self.lowest_row

    def get_max_row_boundary(self):
        if self.agent_height == 1:
            return self.lowest_row
        else:
            return self.lowest_row + self.agent_height - 1

    def get_row_boundaries(self) -> tuple:
        return (self.lowest_row, self.get_max_row_boundary())

    # TODO create agent subclass for player, enemy, and bullet

class PlayerAgent(Agent):
    def __init__(self, agent_length = 1, agent_height = 1, lowest_row = 0, least_col = 0):
        super().__init__(agent_length, agent_height, lowest_row, least_col)

    def get_all_possible_raw_actions(self) -> list(Movements):
        return [Movements.UP, Movements.LEFT, Movements.RIGHT, Movements.DOWN, Movements.STOP]

    def isPlayerAgent(self):
        return True

    #TODO write this, maybe make an action class and action sequence class
    # def takeAction(self, movement):
    #     if movement == Movements.UP:
    #         updated_least_row = self.lowest_row + 1
    #     elif movement == Movements.DOWN
