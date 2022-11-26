import random

from Model.GameState import GameState
from Model.Agents.Actions import Actions
from Model.Agents.AgentSuperClass import AgentSuperClass


class EnemyMoveFireHeuristicAgent(AgentSuperClass):
    """
    This agent can move left, down, up, or fire
    """
    #

    #TODO: CHANGE THIS TO TAKE THE WHOLE GAME STATE
    #TODO: CHANGE TAKE_ACTION TO USE GAMESTATE
    def __init__(self, lowest_row, least_col):
        super().__init__(1, 1, lowest_row, least_col)


    #TODO: Override auto pick action method --> Change this to a list of all possible actions
    def get_all_possible_raw_actions(self) -> list:

        allactions = [Actions.LEFT, Actions.DOWN, Actions.UP, Actions.RIGHT,
                      Actions.FIRE, Actions.FIREUP, Actions.FIREDOWN, Actions.FIRELEFT,
                      Actions.FIRERIGHT]
        return allactions

    def isPlayer(self):
        return False

    def deepcopy(self):
        copy = EnemyMoveFireHeuristicAgent(self.lowest_row, self.least_col)
        copy.hasAlreadyMoved = self.hasAlreadyMoved
        return copy


    def autoPickAction(self, state: GameState = None) -> Actions:
        """
        Picks one of potentially many pre-defined actions randomly
        in a uniform distribution.
        :return:
        """
        #extract player agent position from state
        if state is None:
            raise ValueError("GameState cannot be None for Heuristic Agent")
        player_y, player_x = state.getPlayerPos()
        playerAgent = state.getPlayer();
        if self.is_same_height_agent(playerAgent):
            ideal_pos = player_x + 2
            if self.least_col < ideal_pos:
                allActions = [Actions.FIRERIGHT]
            elif self.least_col > ideal_pos:
                allActions = [Actions.FIRELEFT]
            else:
                return Actions.FIRE

        if self.lowest_row > player_y:
            allActions = [Actions.FIREDOWN, Actions.DOWN]
        elif self.lowest_row < player_y:
            allActions = [Actions.FIREUP, Actions.UP]
        return random.choice(allActions)

    def isHeuristicAgent(self) -> bool:
        '''
        Returns True if agent requires player as a variable
        :return: {bool} Returns True if player variable requires updating, otherwise false
        '''
        return True

    def take_action(self, action: Actions):
        if action in self.get_all_possible_raw_actions():
            agent_copy = self.deepcopy()
            agent_copy.performAction(action)
            agent_copy.hasAlreadyMoved = True
            return agent_copy
        else:
            return self
