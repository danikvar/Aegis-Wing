"""
The agent superclass.
This class defines shared methods between all agents.
"""
from Actions import Actions
from AgentInterface import AgentInterface


class AgentAbstractClass(AgentInterface):
    """
    This is the abstract class for all agents. It has the
    methods and attributes common to all agents and implements
    the AgentInterface.
    """

    def __init__(self, agent_length=1, agent_height=1, lowest_row=0, least_col=0, hp=1):
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
        self.hp = 1 # default hp is 1

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
        return False


    def get_min_col_boundary(self):
        '''
        Gets the minimum col/x value of the agent
        :return: {int} the minimum col/x value of the agent
        '''
        return self.least_col

    def get_max_col_boundary(self):
        """
        Returns the maximum col/x value of the agent
        :return: {int} the maximum col/x value of the agent
        """
        if self.agent_length == 1:
            return self.least_col
        else:
            # i.e. if pos_x = 2
            # and agent_len_x = 3
            # spaced taken up is x = 2,3,4
            # 2 + 3 = 5, 5 is empty space
            return self.least_col + self.agent_length - 1

    def get_col_boundaries(self) -> tuple:
        """
        Returns the column/x boundaries of the agent as a tuple
        :return: {tuple} (agent_x_min, agent_c_max)
        """
        return (self.least_col, self.get_max_col_boundary())

    def get_min_row_boundary(self) -> int:
        """
        Returns the
        :return:
        """

        return self.lowest_row

    def get_max_row_boundary(self) -> int:
        if self.agent_height == 1:
            return self.lowest_row
        else:
            return self.lowest_row + self.agent_height - 1

    def get_row_boundaries(self) -> tuple:
        return (self.lowest_row, self.get_max_row_boundary())

    def set_hp(self, new_hp: int) ->None:
        self.hp = new_hp

    def get_hp(self) -> int:
        return self.hp

    def is_dead(self) -> bool:
        if self.hp < 1:
            return True
        return False

    def performAction(self,action: Actions) -> None:
        """
        Helper method to takeAction method that will be defined
        by subclasses
        :param action: {Actions} action taken
        :return: None
        """
        if action == Actions.UP: #moving up so going up one row
            self.set_position(self.lowest_row + 1, self.least_col)
        elif action == Actions.DOWN:
            self.set_position(self.lowest_row - 1, self.least_col)
        elif action == Actions.LEFT: # move left so move back one col, y - 1
            self.set_position(self.lowest_row, self.least_col - 1)
        elif action == Actions.RIGHT:
            self.set_position(self.lowest_row, self.least_col + 1)
        #TODO maybe have a has fired attribute??

    def is_overlapping_other_agent(self, other_agent: AgentInterface) -> bool:
        current_agent_row_min = self.get_min_row_boundary()
        current_agent_row_max = self.get_max_row_boundary()
        current_agent_col_min = self.get_min_col_boundary()
        current_agent_col_max = self.get_max_col_boundary()

        other_agent_row_min = other_agent.get_min_row_boundary()
        other_agent_row_max = other_agent.get_max_row_boundary()
        other_agent_col_min = other_agent.get_min_col_boundary()
        other_agent_col_max = other_agent.get_max_col_boundary()

        #check if current agent min row overlaps with other agent
        if (current_agent_row_min >= other_agent_row_min
                and current_agent_row_min <= other_agent_row_max):
            #check if current agent max row overlaps with other agent
            if (current_agent_row_max >= other_agent_row_min
                and current_agent_row_max <= other_agent_row_max):
                # check if current agent col min overlaps
                if (current_agent_col_min >= other_agent_col_min
                        and current_agent_col_min <= other_agent_col_max):
                    return True
                # check if current agent col max overlaps
                elif (current_agent_col_min >= other_agent_col_min
                        and current_agent_col_min <= other_agent_col_max):
                    return True
                else:
                    # agents don't overlap
                    return False





class PlayerAgent(AgentAbstractClass):
    def __init__(self, agent_length = 1, agent_height = 1, lowest_row = 0, least_col = 0):
        super().__init__(agent_length, agent_height, lowest_row, least_col)
        self.isInvulnerable = False
        self.turnsUntilInvulnerabilityOver = 0
        self.crossedLeftBounds = False

    def get_all_possible_raw_actions(self) -> list:
        """
        The player agent should be able to perform all actions
        :return: {list(Action)}
        """
        return [Actions.UP, Actions.LEFT, Actions.RIGHT, Actions.DOWN, Actions.STOP, Actions.FIRE]

    def isPlayer(self) -> bool:
        """
        Since this is a player agent it should return True
        :return: {bool} true
        """
        return True

    def copy_agent(self):
        """
        Creates a deep copy of the player agent. This is a helper method
        to takeAction method
        :return:
        """
        return PlayerAgent(self.agent_length,self.agent_height,self.lowest_row, self.least_col)

    def take_action(self, action: Actions):
        agentCopy = self.copy_agent()
        agentCopy.performAction(action)
        return agentCopy


#TODO write tests for this
class SimpleGoLeftAgent(AgentAbstractClass):
    def __init__(self, lowest_row, least_col):
        super().__init__(1, 1, lowest_row, least_col)

    def get_all_possible_raw_actions(self) -> list:
        return [Actions.LEFT]

    def isPlayer(self):
        return False

    def copy_agent(self):
        return SimpleGoLeftAgent(self.lowest_row, self.least_col)

    def take_action(self, action: Actions):
        # check if action is valid
        if action in self.get_all_possible_raw_actions():
            agent_copy = self.copy_agent()
            return agent_copy.performAction(action)
        else:
            return self

