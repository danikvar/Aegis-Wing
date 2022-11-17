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
            #this bullet was fired from player agent
            self.agent_is_player_flag = True
        else:
            action_to_take = Actions.LEFT
            #this bullet was fired by enemy agent
            self.agent_is_player_flag = False

        self.direction = action_to_take

        if speed <= 0:
            raise ValueError("Speed of a prohectile cannot be less than 1")

        super().__init__(action_to_take, projectile_length=1, projectile_height=1, hp=1, speed = speed)

        reference_agent_pos = currentAgent.get_position()
        self.lowest_row = reference_agent_pos[0]

        self.all_possible_raw_actions = None

        #set position of bullet
        if self.agent_is_player_flag:
            #must be placed one col ahead of player agent
            self.least_col = reference_agent_pos[1] + 1
            self.all_possible_raw_actions = [Actions.RIGHT]
        else:
            self.least_col = reference_agent_pos[1] - 1
            self.all_possible_raw_actions = [Actions.LEFT]

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

    def get_all_possible_raw_actions(self) -> list:
        return self.all_possible_raw_actions

    def performAction(self,action: Actions) -> None:
        """
        Helper method to takeAction method that will be defined
        by subclasses
        :param action: {Actions} action taken
        :return: None
        """

        if self.agent_is_player_flag == True:
            if action == Actions.RIGHT:
                self.set_position(self.lowest_row, self.least_col + self.speed)
            else:
                raise RuntimeError(f"Action: {action} is invalid for bullet agent, only Actions.Right is valid")

        else:
            if action == Actions.LEFT:
                self.set_position(self.lowest_row, self.least_col - self.speed)
            else:
                raise RuntimeError(f"Action: {action} is invalid for bullet agent, only Actions.Left is valid")

    def autoPickAction(self) -> Actions:
        return self.get_all_possible_raw_actions()[0]

    def didHitAgent(self, agent: AgentInterface):
        #player cannot hit player and enemy cannot hit enemy
        if self.agent_is_player_flag == agent.isPlayer():
            return False

        #copy bullets, each taking up one x,y pos on grid representing hitting any agents in that path
        copy_bullets = []

        counter = 0
        for i in range(len(self.speed) - 1):
            copied_bullet : SimpleAgentBullet = self.copy()
            if self.agent_is_player_flag:
                copied_bullet.least_col = self.least_col + counter
                counter += 1
            else:
                copied_bullet.least_col = self.least_col - counter
                counter -= 1
            copy_bullets.append(copied_bullet)

        hit_flag = False

        for bullet in copy_bullets:
            each_bullet: SimpleAgentBullet = bullet
            if each_bullet.is_overlapping_other_agent(agent):
                hit_flag = True
                break

        return hit_flag







