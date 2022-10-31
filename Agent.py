"""
The agent superclass.
This class defines shared methods between all agents.
"""
from Actions import Actions

class Agent:
   '''
   This is the abstract class for all agents. It has the
   methods and attributes common to all agents
   '''

    def __init__(self, agent_length=1, agent_height=1, lowest_row=0, least_col=0):
        '''
        Create a new Agent. Warning this code does not reinforce
        whether agents can be outside of board. We need to allow it
        to allow agents to come in from outside the board.
        :param agent_length: {int} length of agent (cannot be < 1)
        :param agent_height: {int} height of agent (cannot be > 1)
        :param lowest_row: {int} position of the lowest "y" or row value for an agent
        :param least_col: {int} position of the lowest "x" or column value for the agent
        '''
        if agent_length < 1:
            raise ValueError("Agent size length must be >= 1")
        if agent_height < 1:
            raise ValueError("Agent size height must be >= 1")

        # possible case where enemies start at edge of board or even behind it?
        self.crossedStartingBounds = False
        self.agent_length = agent_length
        self.agent_height = agent_height
        # position of least left
        self.lowest_row = lowest_row
        # position of lowest side
        self.least_col = least_col
        # if player agent set to True
        self.isPlayer = False

    def get_position(self) -> tuple:
        '''
        Returns a tuple representing lowest left x position
        and lowest y position
        :return: {tuple} (furthest left x post, highest y pos)
        '''
        return (self.lowest_row, self.least_col)

    def set_position(self, lowest_row: int, least_col: int) -> None:
        '''
        Sets the position of the agents
        :param lowest_row: {int} position of the lowest "y" or row value for an agent
        :param least_col: {int} position of the lowest "x" or column value for the agent
        :return:
        '''
        self.lowest_row = lowest_row
        self.least_col = least_col

    def get_agent_size(self) -> tuple:
        '''
        Returns the size of the agent as a tuple
        :return: {tuple} (agent length, agent_height)
        '''
        return (self.agent_length, self.agent_height)

    def isPlayer(self):
        '''
        Returns True if player agent, otherwise false
        :return: {bool} Returns True if player agent, otherwise false
        '''
        return self.isPlayer


    def get_min_col_boundary(self):
        '''
        Gets the minimum col/x value of the agent
        :return: {int} the minimum col/x value of the agent
        '''
        return self.least_col

    def get_max_col_boundary(self):
        '''
        Returns the maximum col/x value of the agent
        :return: {int} the maximum col/x value of the agent
        '''
        if self.agent_length == 1:
            return self.least_col
        else:
            # i.e. if pos_x = 2
            # and agent_len_x = 3
            # spaced taken up is x = 2,3,4
            # 2 + 3 = 5, 5 is empty space
            return self.least_col + self.agent_length - 1

    def get_min_row_boundary(self) -> int:
        return self.lowest_row

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
        self.isInvulnerable = False
        self.turnsUntilInvulnerabilityOver = 0
        self.crossedLeftBounds = False
        self.isPlayer = True


    def set_position(self, lowest_row: int, least_col: int):
        # if you agent finally on board
        if (self.crossedLeftBounds):
            if (lowest_row < 0 or least_col < 0):
                raise RuntimeError("Agent cannot go off board")

    def get_all_possible_raw_actions(self) -> list:
        return [Actions.UP, Actions.LEFT, Actions.RIGHT, Actions.DOWN, Actions.STOP, Actions.FIRE]

    def isPlayerAgent(self):
        return True

    #TODO write this, maybe make an action class and action sequence class
    def takeLegalAction(self, movement: Actions):
        if movement == Actions.UP: #if moving up
            #check if moving up will cause player to go beyond upper boundary

            self.lowest_row = self.lowest_row + 1
        elif movement == Actions.DOWN:
            self.lowest_row = self.lowest_row - 1

