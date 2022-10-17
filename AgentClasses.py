from Agent import Agent

class PlayerAgent(Agent):
    def __init__(self, agent_length = 1, agent_height = 1, lowest_row = 0, least_col = 0):
        super().__init__(agent_length, agent_height, lowest_row, least_col)