from Model.Agents.AgentInterface import AgentInterface
from Model.Agents.AgentSuperClass import AgentSuperClass
from Model.Agents.Directions import Directions


class ProjectileInterface(AgentSuperClass):

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

    def didHitAgent(self,agent: AgentInterface) -> bool:
        raise NotImplementedError