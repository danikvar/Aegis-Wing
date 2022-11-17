"""
The agent superclass.
This class defines shared methods between all agents.
"""
from Model.Agents.Actions import Actions
from Model.Agents.AgentInterface import AgentInterface
from Model.Agents.AgentSuperClass import AgentSuperClass


class ProjectileSuperClass(AgentSuperClass):
    """
    This is the abstract class for all projectiles. It is extending the Agent
    super class.
    """

    def __init__(self, direction: Actions, projectile_length=1, projectile_height=1, lowest_row=0, least_col=0, hp=1,
                speed = 1):

        super().__init__(projectile_length, projectile_height, lowest_row, least_col, hp)
        self.speed = speed
        self.direction = direction


    def changeSpeed(self, speed: int):
        """
        Changes the number of spaces that the projectile moves each turn.
        Will be used if we want to create complex projectiles
        :return: 
        """
        self.speed = speed
        
    def changeDirection(self, direction: Actions) -> None:
        """
        Changes the direction that the projectile moves each turn.
        Will be used if we want to create complex projectiles
        :return: 
        """
        self.direction = direction

    def performAction(self,action: Actions) -> None:
        """
        Helper method to takeAction method that will be defined
        by subclasses
        :param action: {Actions} action taken
        :return: None
        """
        if self.direction == Actions.UP: #moving up so going up one row
            self.set_position(self.lowest_row + self.speed, self.least_col)
        elif self.direction == Actions.DOWN:
            self.set_position(self.lowest_row - self.speed, self.least_col)
        elif self.direction == Actions.LEFT: # move left so move back one col, y - 1
            self.set_position(self.lowest_row, self.least_col - self.speed)
        elif self.direction == Actions.RIGHT:
            self.set_position(self.lowest_row, self.least_col + self.speed)
        #TODO maybe have a has fired attribute??


