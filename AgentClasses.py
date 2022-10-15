from Agent import Agent

class PlayerAgent(Agent):
    def __init__(self,agent_len_x = 1, agent_len_y = 1, pos_x = 0, pos_y = 0):
        super().__init__(agent_len_x, agent_len_y, pos_x, pos_y)