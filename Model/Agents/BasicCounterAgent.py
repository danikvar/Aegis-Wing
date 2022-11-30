import random

from Model.GameState import GameState
from Model.Agents.Actions import Actions
from Model.Agents.AgentSuperClass import AgentSuperClass


class BasicCounterAgent(AgentSuperClass):
    """
    This agent can move left, down, up, or fire.
    This agent
    """


    def __init__(self, lowest_row, least_col, count: int, ideal_x: int, ideal_y: int):
        super().__init__(1, 1, lowest_row, least_col)
        self.counter = count
        self.ideal_x = ideal_x
        self.ideal_y = ideal_y
        self.atIdealPos = False

    def get_all_possible_raw_actions(self) -> list:

        allactions = [Actions.LEFT, Actions.DOWN, Actions.UP, Actions.RIGHT,
                      Actions.FIRE, Actions.FIREUP, Actions.FIREDOWN, Actions.FIRELEFT,
                      Actions.FIRERIGHT]
        return allactions

    def isPlayer(self):
        return False

    def deepcopy(self):
        copy = BasicCounterAgent(self.lowest_row, self.least_col, self.counter, self.ideal_x, self.ideal_y)
        copy.hasAlreadyMoved = self.hasAlreadyMoved
        return copy

    def autoPickAction(self, state: GameState = None) -> Actions:
        """
        If the agent is in the proper position then it stays and fires.
        If not it moves towards that position and increments the counter
            to keep it alive until it reaches position.
        Once the counter is finished it moves left off the screen.
        :return:
        """


        print("Counter is at: " + str(self.counter))
        if self.counter <= 0:
            return Actions.FIRELEFT

        if self.ideal_y == self.lowest_row and self.ideal_x == self.least_col:
            self.counter -= 1
            return Actions.FIRE

        elif self.ideal_y == self.lowest_row:
            print("Increasing Counter1:")

            if self.least_col < self.ideal_x:
                return Actions.FIRERIGHT

            elif self.least_col > self.ideal_x:
                return Actions.FIRELEFT
        else:
            if self.lowest_row < self.ideal_y:
                return Actions.FIREUP

            elif self.lowest_row > self.ideal_y:
                return Actions.FIREDOWN
