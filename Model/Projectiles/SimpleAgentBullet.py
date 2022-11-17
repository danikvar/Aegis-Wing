import uuid

from Model.Agents.Directions import Directions
from Model.Projectiles.ProjectileSuperClass import ProjectileSuperClass


class SimpleAgentBullet(ProjectileSuperClass):
    
    def __init__(self, currentAgent, speed = 1):
        
        
        super().__init__(length=1, height=1, lowest_row=currentAgent.lowest_row, least_col=0, hp=1,
                speed = 1, direction = Directions.LEFT)
      
        self.statPos(currentAgent)
        self.currentAgent = currentAgent
        self.direction = self.startDir(currentAgent)
        self.id = uuid.uuid4()

    def isPlayerBullet(self):
        return self.currentAgent.isPlayer()
    
    def startDir(self, currentAgent):
        if currentAgent.isPlayer():
            self.direction = Directions.RIGHT
        else:
            self.direction = Directions.LEFT
    
    def startPos(self, currentAgent):
        if currentAgent.isPlayer():
            self.least_col = currentAgent.get_max_col_boundary + 1
        else:
            self.least_col = currentAgent.get_min_col_boundary - 1

    def copy(self):
        copy = SimpleAgentBullet(self.lowest_row, self.least_col, self.currentAgent, self.direction)
        copy.hasAlreadyMoved = self.hasAlreadyMoved
        copy.id = self.id
        return copy

    def getId(self):
        return self.id