from Projectiles.Directions import Directions
from Agents.AgentInterface import AgentInterface

class ProjectileInterface:

    '''
    This interface mandates all methods that must be
    implemented by any subtype. The methods must be defined
    by the subtype. Most of these methods will be defined
    in the AgentSuperClass
    '''
    
    def isPlayerBullet(self) -> bool:
        """
        Returns True if projectile was fired from Player Agent, otherwise false
        :return: {bool} True if projectile was fired from Player Agent, otherwise false
        """
        raise NotImplementedError

    def get_position(self) -> tuple:
        """
        Returns a tuple representing lowest left x position
        and lowest y position
        :return: {tuple} (furthest left x post, highest y pos)
        """
        # raising not implemented because the subtype must
        # define this method
        raise NotImplementedError

    def set_position(self, lowest_row: int, least_col: int) -> None:
        """
        Sets the position of the agents
        :param lowest_row: {int} position of the lowest "y" or row value for an agent
        :param least_col: {int} position of the lowest "x" or column value for the agent
        :return:
        """
        raise NotImplementedError

    def get_projectile_size(self) -> tuple:
        """
        Returns the size of the agent as a tuple
        :return: {tuple} (agent length, agent_height)
        """
        raise NotImplementedError

    def changeSpeed(self, speed: int) -> None:
        """
        Changes the number of spaces that the projectile moves each turn.
        Will be used if we want to create complex projectiles
        :return: 
        """
        raise NotImplementedError
        
    def changeDirection(self, direction: Directions) -> None:
        """
        Changes the direction that the projectile moves each turn.
        Will be used if we want to create complex projectiles
        :return: 
        """
        raise NotImplementedError

    def get_min_col_boundary(self) -> int:
        """
        Gets the minimum col/x value of the agent
        :return: {int} the minimum col/x value of the agent
        """
        raise NotImplementedError

    def get_max_col_boundary(self) -> int:
        """
        Returns the maximum col/x value of the agent
        :return: {int} the maximum col/x value of the agent
        """

    def get_min_row_boundary(self) -> int:
        """
        Gets the minimum row/y value of the agent
        :return:  {int} the minimum row/y value of the agent
        """
        raise NotImplementedError

    def get_max_row_boundary(self) -> int:
        """
        Gets the maximum row/y value of the agent
        :return: {int} the maximum row/y value of the agent
        """
        raise NotImplementedError

    def get_col_boundaries(self) -> tuple:
        """
        Retuns a tuple representing the min and max col/x boundaries
        :return: {tuple} (min_x boundary of agent, max_x boundary of agent)
        """
        raise NotImplementedError

    def get_row_boundaries(self) -> tuple:
        """
        Returns a tuple representing the min and max row/y boundaries
        of the agent
        :return:  {tuple} (min_y boundary of agent, max_y boundary of agent)
        """
        raise NotImplementedError


    def get_hp(self)-> int:
        """
        Returns the amount of hp an agent has 
        :return: {int} hp of the agent
        """
        raise NotImplementedError

    def set_hp(self, new_hp: int)->None:
        """
        Sets the current hp of an agent
        :param new_hp: {int} the new hp of the agent
        :return: None
        """
        raise NotImplementedError

    def is_dead(self) -> bool:
        """
        Returns true if current hp = 0, otherwise false
        :return: {bool} true if hp = 0, else false
        """
        raise NotImplementedError

    def copy(self):
        """
        Returns a deepcopy of the agent
        :return: {AgentInterface} a copy of the current agent
        """
        raise NotImplementedError


    def take_action(self, action: Directions):
        """
        Returns a copy of the current agent with the same length and width
        but with a new position caused by an action
        :param action: {Directions} the action that causes an agent to change position
        :return:
        """
        raise NotImplementedError

    def is_overlapping_agent(self, agent: AgentInterface):
        """
        Checks if current agent is overlapping with another agent
        :param agent: {AgentInterface}
        :return: {bool} True if agent overlaps other agent, false otherwise
        """
        raise NotImplementedError

    #TODO write tests
    def hasMoved(self)-> bool:
        """
        Returns true if action was already taken, false otherwise
        :return: {bool} True if already took actions, false otherwise
        """
        raise NotImplementedError

    def resetMoveStatus(self) -> None:
        raise NotImplementedError

    def getId(self):
        raise NotImplementedError