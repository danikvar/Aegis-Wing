"""
The agent superclass.
This class defines shared methods between all agents.
"""
from Projectiles.Directions import Directions
from Projectiles.ProjectileInterface import ProjectileInterface
from Projectiles.ProjectileInterface import AgentInterface

class ProjectileSuperClass(ProjectileInterface):
    """
    This is the abstract class for all projectiles. It has the
    methods and attributes common to all projectiles and implements
    the ProjectileSuperClass.
    """

    def __init__(self, length=1, height=1, lowest_row=0, least_col=0, hp=1,
                speed = 1, direction = Directions.LEFT):
        '''
        Create a new Agent. Warning this code does not reinforce
        whether agents can be outside of board. We need to allow it
        to allow agents to come in from outside the board.
        :param agent_height: {int} height of agent (cannot be > 1)
        :param lowest_row: {int} position of the lowest "y" or row value for an agent
        :param least_col: {int} position of the least (furthest left) "x" or column value for the agent
        '''
        if agent_length < 1:
            raise ValueError("Agent size length must be >= 1")
        if agent_height < 1:
            raise ValueError("Agent size height must be >= 1")

        self.length = length
        self.height = height
        # position of lowest side
        self.lowest_row = lowest_row
        # position of furthest left side
        self.least_col = least_col
        self.hp = hp # default hp is 1
        # default is to move 1 space per turn
        self.speed = speed
        self.direction = direction
        self.hasAlreadyMoved = False

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

    def get_projectile_size(self) -> tuple:
        '''
        Returns the size of the projectile as a tuple
        :return: {tuple} (agent length, agent_height)
        '''
        return (self.length, self.height)

    def changeSpeed(self, speed: int):
        """
        Changes the number of spaces that the projectile moves each turn.
        Will be used if we want to create complex projectiles
        :return: 
        """
        self.speed = speed
        
    def changeDirection(self, direction: Directions) -> None:
        """
        Changes the direction that the projectile moves each turn.
        Will be used if we want to create complex projectiles
        :return: 
        """
        self.direction = direction

    def get_min_col_boundary(self) -> int:
        '''
        Gets the minimum col/x value of the agent
        :return: {int} the minimum col/x value of the agent
        '''
        return self.least_col

    def get_max_col_boundary(self) -> int:
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

    def performAction(self,action: Directions) -> None:
        """
        Helper method to takeAction method that will be defined
        by subclasses
        :param action: {Actions} action taken
        :return: None
        """
        if self.direction == Directions.UP: #moving up so going up one row
            self.set_position(self.lowest_row + this.speed, self.least_col)
        elif self.direction == Directions.DOWN:
            self.set_position(self.lowest_row - this.speed, self.least_col)
        elif self.direction == Directions.LEFT: # move left so move back one col, y - 1
            self.set_position(self.lowest_row, self.least_col - this.speed)
        elif self.direction == Directions.RIGHT:
            self.set_position(self.lowest_row, self.least_col + this.speed)
        #TODO maybe have a has fired attribute??

    def is_overlapping_other(self, other: AgentInterface) -> bool:
        cur_proj_row_min = self.get_min_row_boundary()
        cur_proj_row_max = self.get_max_row_boundary()
        cur_proj_col_min = self.get_min_col_boundary()
        cur_proj_col_max = self.get_max_col_boundary()

        other_row_min = other.get_min_row_boundary()
        other_row_max = other.get_max_row_boundary()
        other_col_min = other.get_min_col_boundary()
        other_col_max = other.get_max_col_boundary()

        #check if current agent min row overlaps with other agent
        if (cur_proj_row_min >= other_row_min
                and cur_proj_row_min <= other_row_max):
            #check if current agent max row overlaps with other agent
            if (cur_proj_row_max >= other_row_min
                and cur_proj_row_max <= other_row_max):
                # check if current agent col min overlaps
                if (cur_proj_col_min >= other_col_min
                        and cur_proj_col_min <= other_col_max):
                    return True
                # check if current agent col max overlaps
                elif (cur_proj_col_max >= other_col_min
                        and cur_proj_col_max <= other_col_max):
                    return True
                else:
                    # agents don't overlap
                    return False

    #TODO write tests, also haven't really incorporated this
    # maybe use in checkAgentClashes???
    def hasMoved(self) -> bool:
        return self.hasAlreadyMoved

    def resetMoveStatus(self) -> None:
        self.hasAlreadyMoved = False

    def take_action(self, action: Directions):
        if action == self.direction:
            projCopy = self.copy()
            projCopy.performAction(action)
            projCopy.hasAlreadyMoved = True
            return projCopy
        else:
            return self


