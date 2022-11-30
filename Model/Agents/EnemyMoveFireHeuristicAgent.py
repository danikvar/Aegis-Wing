import random

from Model.GameState import GameState
from Model.Agents.Actions import Actions
from Model.Agents.AgentSuperClass import AgentSuperClass


class EnemyMoveFireHeuristicAgent(AgentSuperClass):
    """
    This agent can move left, down, up, or fire
    """

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
        agent_copy = self.deepcopy()
        list_enemy_agents = state.current_agents[1:]

        list_enemy_agents.remove(self)

        #extract player agent position from state
        if state is None:
            raise ValueError("GameState cannot be None for Heuristic Agent")
        player_y, player_x = state.getPlayerPos()
        playerAgent = state.getPlayer();
        ideal_pos = player_x + 2

        if self.is_same_height_agent(playerAgent):
            if ideal_pos > self.least_col > player_x - 4:
                allActions = [Actions.FIREDOWN, Actions.FIREUP]
                # TODO: Dan - Look at issue if player highest or lowest to change the up/down action
                # TODO: Dan - Give chance of crashing into player
            elif self.least_col < ideal_pos:
                agent_copy.performAction(Actions.RIGHT)
                overlaps = any([self.is_overlapping_other_agent(other) for other in list_enemy_agents])
                agent_copy.performAction(Actions.LEFT)
                if overlaps:
                    allActions = [Actions.FIRERIGHT, Actions.FIREUP, Actions.FIREDOWN]
                else:
                    allActions = [Actions.FIRERIGHT]
            elif self.least_col > ideal_pos:
                agent_copy.performAction(Actions.LEFT)
                overlaps = any([self.is_overlapping_other_agent(other) for other in list_enemy_agents])
                agent_copy.performAction(Actions.RIGHT)
                if overlaps:
                    allActions = [Actions.FIRERIGHT, Actions.FIRELEFT, Actions.FIRE, Actions.FIREUP, Actions.FIREDOWN]
                else:
                    allActions = [Actions.FIRELEFT]
            else:
                allActions = [Actions.FIRE, Actions.FIRERIGHT]

        if self.lowest_row > player_y:
            if ideal_pos > self.least_col > player_x - 4:
                return Actions.FIRERIGHT
            agent_copy.performAction(Actions.DOWN)
            overlaps = any([self.is_overlapping_other_agent(other) for other in list_enemy_agents])
            agent_copy.performAction(Actions.UP)
            if overlaps:
                allActions = [Actions.FIREDOWN, Actions.FIRERIGHT, Actions.FIRE]
            else:
                allActions = [Actions.FIREDOWN]
        elif self.lowest_row < player_y:
            if ideal_pos > self.least_col > player_x - 4:
                return Actions.FIRERIGHT
            agent_copy.performAction(Actions.UP)
            overlaps = any([self.is_overlapping_other_agent(other) for other in list_enemy_agents])
            agent_copy.performAction(Actions.DOWN)
            if overlaps:
                allActions = [Actions.FIREUP, Actions.FIRERIGHT, Actions.FIRE]
            else:
                allActions = [Actions.FIREUP]

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
