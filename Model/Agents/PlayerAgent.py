from Model.Agents.Actions import Actions
from Model.Agents.AgentSuperClass import AgentSuperClass


class PlayerAgent(AgentSuperClass):
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