"""
The agent superclass.
This class defines shared methods between all agents.
"""
class Agent:
    def __init__(self, agent_len_x = 1, agent_len_y = 1, pos_x = 0, pos_y = 0):
        if agent_len_x < 1:
            raise ValueError("Agent size length must be greater than 1")
        if agent_len_y < 1:
            raise ValueError("Agent size height must be grater than 1")

        if pos_x < 0:
            raise ValueError('Agent cannot start at any x position less than 0, (leftmost limit)')
        if pos_y:
            raise ValueError('Agent cannot start at any y position less than 0 (bottom limit)')

        #possible case where enemies start at edge of board or even behind it?

        self.agent_len_x = agent_len_x
        self.agent_len_y = agent_len_y
        #position of most furthest right side
        self.pos_x = pos_x
        #position of most furthest upper side
        self.pos_y = pos_y

    def get_position(self) -> tuple:
        return (self.pos_x, self.pos_y)

    def get_agent_size(self) -> tuple:
        return (self.agent_len_x,self.agent_len_y)

    def get_min_x_boundary(self) -> int:
        if self.agent_len_x == 1:
            return self.pos_x
        else:
            return self.pos_x - self.agent_len_x

    def get_x_boundaries(self) -> dict:
        '''
        This function returns info regarding the x axis boundaries of the ship/agent
        All ships/agents will be rectangle shaped
        :return: {dict} where keys are "min" and "max" and the values
                    are the minimum x boundary and maximum x boundary
        '''
        return{"min": self.get_min_x_boundary(), "max": self.pos_x}

    def get_min_y_boundary(self) -> int:
        if self.agent_len_y == 1:
            return self.pos_y
        else:
            return self.pos_y - self.agent_len_y

    def get_y_boundaries(self)->dict:
        '''
        This function returns info regarding the y axis boundaries of the ship/agent
        All ships/agents will be rectangle shaped
        :return: {dict} where keys are "min" and "max" and the values
                    are the minimum y boundary and maximum y boundary
        :return:
        '''
        return {"min": self.get_min_y_boundary(), "max": self.pos_y}






