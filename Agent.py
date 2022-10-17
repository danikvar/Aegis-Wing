"""
The agent superclass.
This class defines shared methods between all agents.
"""


class Agent:
    def __init__(self, agent_len_x=1, agent_len_y=1, pos_x=0, pos_y=0):
        if agent_len_x < 1:
            raise ValueError("Agent size length must be >= 1")
        if agent_len_y < 1:
            raise ValueError("Agent size height must be >= 1")

        if pos_x < 0:
            raise ValueError('Agent cannot start at any x position less than 0, (leftmost limit)')
        if pos_y < 0:
            raise ValueError('Agent cannot start at any y position less than 0 (bottom limit)')

        # possible case where enemies start at edge of board or even behind it?

        self.agent_len_x = agent_len_x
        self.agent_len_y = agent_len_y
        # position of most furthest right side
        self.pos_x = pos_x
        # position of most furthest upper side
        self.pos_y = pos_y

    def get_position(self) -> tuple:
        '''
        Returns a tuple representing lowest left x position
        and lowest y position
        :return: {tuple} (lowest x post, lowest y pos)
        '''
        return (self.pos_x, self.pos_y)

    def get_agent_size(self) -> tuple:
        return (self.agent_len_x, self.agent_len_y)


    def get_min_x_boundary(self):
        return self.pos_x

    def get_max_x_boundary(self):
        if self.agent_len_x == 1:
            return self.pos_x
        else:
            # i.e. if pos_x = 2
            # and agent_len_x = 3
            # spaced taken up is x = 2,3,4
            # 2 + 3 = 5, 5 is empty space
            return self.pos_x + self.agent_len_x - 1

    def get_x_boundaries(self) -> tuple:

        return (self.pos_x, self.get_max_x_boundary())

    def get_min_y_boundary(self) -> int:
        return self.pos_y

    def get_max_y_boundary(self):
        if self.agent_len_y == 1:
            return self.pos_y
        else:
            return self.pos_y + self.agent_len_y - 1

    def get_y_boundaries(self) -> tuple:
        return (self.pos_y, self.get_max_y_boundary())

    # TODO create agent subclass for player, enemy, and bullet
