
#TODO write tests for this
import uuid

from Model.Agents.Actions import Actions
from Model.Agents.AgentSuperClass import AgentSuperClass


class SimpleGoLeftAgent(AgentSuperClass):
    def __init__(self, lowest_row, least_col):
        super().__init__(1, 1, lowest_row, least_col)
        self.id = uuid.uuid4()

    def get_all_possible_raw_actions(self) -> list:
        return [Actions.LEFT]

    def isPlayer(self):
        return False

    def copy(self):
        copy = SimpleGoLeftAgent(self.lowest_row, self.least_col)
        copy.hasAlreadyMoved = self.hasAlreadyMoved
        copy.id = self.id
        return copy

    # def take_action(self, action: Actions):
    #     # check if action is valid
    #     if action in self.get_all_possible_raw_actions():
    #         agent_copy = self.copy()
    #         agent_copy.performAction(action)
    #         agent_copy.hasAlreadyMoved = True
    #         return agent_copy
    #     else:
    #         return self

    def autoPickAction(self) -> Actions:
        """
        Picks one of potentially many pre-defined actions.
        :return:
        """
        return self.get_all_possible_raw_actions()[0]

    def getId(self):
        return self.id