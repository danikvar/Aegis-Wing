import uuid

from Model.Agents.Actions import Actions
from Model.Agents.AgentInterface import AgentInterface
from Model.Agents.Directions import Directions
from Model.Agents.PlayerAgent import PlayerAgent
from Model.Projectiles.ProjectileSuperClass import ProjectileSuperClass


class SimpleAgentBullet(ProjectileSuperClass):
    
    def __init__(self, currentAgent: AgentInterface, speed = 1):

        action_to_take = None

        #default motion for simple bullet
        if currentAgent.isPlayer():
            action_to_take = Actions.RIGHT
            self.agent_is_player_flag = True
        else:
            action_to_take = Actions.LEFT
            self.agent_is_player_flag = False

        self.direction = action_to_take

        super().__init__(action_to_take, projectile_length=1, projectile_height=1, hp=1, speed = speed)

        reference_agent_pos = currentAgent.get_position()
        self.lowest_row = reference_agent_pos[0]

        #set position of bullet
        if self.agent_is_player_flag:
            #must be placed one col ahead of player agent
            self.least_col = reference_agent_pos[1] + 1
        else:
            self.least_col = reference_agent_pos[1] - 1


    def isPlayer(self) -> bool:
        #is a bullet this method does not apply
        raise RuntimeError('A bullet is not a player or enemy agent, cannot call isPlayer on a ProjectileSuperClass type object')


    def isPlayerBullet(self):
        return self.agent_is_player_flag


    def copy(self):
        #agent placeholder, need it since constructor relies on an AgentInterface
        # will override values to match original SimpleBulletAgent
        placeholder = PlayerAgent()
        copy = SimpleAgentBullet(placeholder,self.speed)
        copy.least_col = self.least_col
        copy.lowest_row = self.lowest_row
        copy.agent_is_player_flag = self.agent_is_player_flag
        copy.direction = self.direction

