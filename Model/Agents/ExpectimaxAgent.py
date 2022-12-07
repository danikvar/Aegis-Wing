import uuid
import random
from math import inf

from Model.GameState import GameState
from Model.Agents.Actions import Actions
from Model.Agents.AgentSuperClass import AgentSuperClass


class ExpectimaxAgent(AgentSuperClass):
    def __init__(self, agent_length: int = 1, agent_height: int = 1, lowest_row: int = 1, least_col: int = 1, count: int = 10):
        super().__init__(agent_length, agent_height, lowest_row, least_col)
        self.counter = count
        self.id = uuid.uuid4()
        self.depth = None

    def get_all_possible_raw_actions(self) -> list:
        allactions = [Actions.STOP, Actions.UP, Actions.DOWN, Actions.LEFT, Actions.RIGHT,
                      Actions.FIRE]
        return allactions

    def isPlayer(self):
        return True

    def deepcopy(self):
        copy = ExpectimaxAgent(self.agent_length,self.agent_height, self.lowest_row, self.least_col, count=self.counter)
        copy.hasAlreadyMoved = self.hasAlreadyMoved
        copy.id = self.id
        return copy

    def respawnPlayer(self):
        return ExpectimaxAgent(self.agent_length,self.agent_height,self.spawn_y, self.spawn_x, count=self.counter)


    def autoPickAction(self, state: GameState = None) -> Actions:
        """
        Picks one of potentially many pre-defined actions randomly
        in a uniform distribution.
        :return:
        """

        if self.counter is not None and self.counter <= 0:
            return Actions.FIRERIGHT

        agent_copy = self.deepcopy()
        list_enemy_agents = state.current_agents

        # extract player agent position from state
        if state is None:
            raise ValueError("GameState cannot be None for Expectimax Agent")
        # player_y, player_x = state.getPlayerPos()
        # playerAgent = state.getPlayer()
        # ideal_pos = player_x + 2
        #
        # print(playerAgent)
        # print(state.gameBoard.getBoardBoundaries())

        boardColMin = state.gameBoard.getBoardBoundaries()[0]
        boardColMax = state.gameBoard.getBoardBoundaries()[1]
        boardRowMin = state.gameBoard.getBoardBoundaries()[2]
        boardRowMax = state.gameBoard.getBoardBoundaries()[3]

        # print(boardColMin, boardColMax, boardRowMin, boardRowMax)
        # print(self.get_col_boundaries(), self.get_row_boundaries())

        #Get all legal actions of player, arg is 0 because player index is 0
        legalActions = state.getAllLegalActions(0)
        print("PLAYER ACTIONS: ", legalActions)
        #get current score of state
        score = state.score
        print("SCORE:", score)

        # generate a new state per legal agent actions
        actionScoreDictionary = {}
        for playerAction in legalActions:
            print()
            print(playerAction)
            new_state = state.generateSuccessorState(0, playerAction)
            #score of state where player agent has moved to a new position, but no enemies have moved yet
            playerScore = new_state.score
            # print("PLAYER SCORE DEPTH 1 = ", playerScore)

            #for each enemy have them make a move
            #get all enemies
            #THIS is an example, it's not a 1:1

            expectedEnemyValue = 0
            allEnemyAgentsList = new_state.current_agents[1:]
            # print(allEnemyAgentsList)
            for eachEnemyIndex in range(len(allEnemyAgentsList)):
                true_enemy_index = eachEnemyIndex + 1
                # print()
                # print("ENEMY # ", true_enemy_index)
                all_legal_enemy_actions = new_state.getAllLegalActions(true_enemy_index)
                # print(all_legal_enemy_actions)

                for each_enemy_action in all_legal_enemy_actions:
                    enemyMoveState = new_state.generateSuccessorState(true_enemy_index,each_enemy_action)
                    enemyScore = enemyMoveState.score

                    expectedEnemyValue += enemyScore

                    # print("ACTION: ", each_enemy_action, "ENEMY SCORE: ", enemyScore, "EXPECTED ENEMY VAL", expectedEnemyValue)

            actionScoreDictionary[playerAction] = expectedEnemyValue
            print(actionScoreDictionary)

        bestAction = max(actionScoreDictionary, key=actionScoreDictionary.get)
        print("BEST ACTION", bestAction)

        # action = random.choice(legalActions)
        action = bestAction
        print()


                    #if enemies are minimizer nodes, then you need to go from minimizer node -> minimizer node until all enemies have moved
                    #then you can go the the next depth

        # if (self.get_min_row_boundary() <= boardRowMin) and (self.get_min_col_boundary() <= boardColMin):
        #     legalActions = [Actions.STOP, Actions.UP, Actions.RIGHT, Actions.FIRE]
        #     action = random.choice(legalActions)
        #     agent_copy.performAction(action)
        #     print("MIN ROW MIN COL", action)
        # elif (self.get_max_row_boundary() >= boardRowMax) and (self.get_min_col_boundary() <= boardColMin):
        #     legalActions = [Actions.STOP, Actions.DOWN, Actions.RIGHT, Actions.FIRE]
        #     action = random.choice(legalActions)
        #     agent_copy.performAction(action)
        #     print("MAX ROW MIN COL", action)
        # elif (self.get_min_row_boundary() <= boardRowMin) and (self.get_max_col_boundary() >= boardColMax):
        #     legalActions = [Actions.STOP, Actions.UP, Actions.LEFT, Actions.FIRE]
        #     action = random.choice(legalActions)
        #     agent_copy.performAction(action)
        #     print("MIN ROW MAX COL", action)
        # elif (self.get_max_row_boundary() >= boardRowMax) and (self.get_max_col_boundary() >= boardColMax):
        #     legalActions = [Actions.STOP, Actions.DOWN, Actions.LEFT, Actions.FIRE]
        #     action = random.choice(legalActions)
        #     agent_copy.performAction(action)
        #     print("MAX ROW MAX COL", action)
        # elif self.get_min_row_boundary() <= boardRowMin:
        #     legalActions = [Actions.STOP, Actions.UP, Actions.LEFT, Actions.RIGHT, Actions.FIRE]
        #     action = random.choice(legalActions)
        #     agent_copy.performAction(action)
        #     print("MIN ROW", action)
        # elif self.get_max_row_boundary() >= boardRowMax:
        #     legalActions = [Actions.STOP, Actions.DOWN, Actions.LEFT, Actions.RIGHT, Actions.FIRE]
        #     action = random.choice(legalActions)
        #     agent_copy.performAction(action)
        #     print("MAX ROW", action)
        # elif self.get_min_col_boundary() <= boardColMin:
        #     legalActions = [Actions.STOP, Actions.UP, Actions.DOWN, Actions.RIGHT, Actions.FIRE]
        #     action = random.choice(legalActions)
        #     agent_copy.performAction(action)
        #     print("MIN COL", action)
        # elif self.get_max_col_boundary() >= boardColMax:
        #     legalActions = [Actions.STOP, Actions.UP, Actions.DOWN, Actions.LEFT, Actions.FIRE]
        #     action = random.choice(legalActions)
        #     agent_copy.performAction(action)
        #     print("MAX COL", action)
        # else:
        #     legalActions = [Actions.STOP, Actions.UP, Actions.DOWN, Actions.LEFT, Actions.RIGHT, Actions.FIRE]
        #     action = random.choice(legalActions)
        #     agent_copy.performAction(action)
        #     print("ELSE", action)



        # if self.is_same_height_agent(playerAgent):
        #     if ideal_pos > self.least_col > player_x - 4:
        #         allActions = [Actions.FIREDOWN, Actions.FIREUP]
        #     elif self.least_col < ideal_pos:
        #         agent_copy.performAction(Actions.RIGHT)
        #         overlaps = any([self.is_overlapping_other_agent(other) for other in list_enemy_agents])
        #         agent_copy.performAction(Actions.LEFT)
        #         if overlaps:
        #             allActions = [Actions.FIRERIGHT, Actions.FIREUP, Actions.FIREDOWN]
        #         else:
        #             allActions = [Actions.FIRERIGHT]
        #     elif self.least_col > ideal_pos:
        #         agent_copy.performAction(Actions.LEFT)
        #         overlaps = any([self.is_overlapping_other_agent(other) for other in list_enemy_agents])
        #         agent_copy.performAction(Actions.RIGHT)
        #         if overlaps:
        #             allActions = [Actions.FIRERIGHT, Actions.FIRELEFT, Actions.FIRE, Actions.FIREUP, Actions.FIREDOWN]
        #         else:
        #             allActions = [Actions.FIRELEFT]
        #     else:
        #         allActions = [Actions.FIRE, Actions.FIRERIGHT]
        #
        # if self.lowest_row > player_y:
        #     if ideal_pos > self.least_col > player_x - 4:
        #         return Actions.FIRERIGHT
        #     agent_copy.performAction(Actions.DOWN)
        #     overlaps = any([self.is_overlapping_other_agent(other) for other in list_enemy_agents])
        #     agent_copy.performAction(Actions.UP)
        #     if overlaps:
        #         allActions = [Actions.FIREDOWN, Actions.FIRERIGHT, Actions.FIRE]
        #     else:
        #         allActions = [Actions.FIREDOWN]
        # elif self.lowest_row < player_y:
        #     if ideal_pos > self.least_col > player_x - 4:
        #         return Actions.FIRERIGHT
        #     agent_copy.performAction(Actions.UP)
        #     overlaps = any([self.is_overlapping_other_agent(other) for other in list_enemy_agents])
        #     agent_copy.performAction(Actions.DOWN)
        #     if overlaps:
        #         allActions = [Actions.FIREUP, Actions.FIRERIGHT, Actions.FIRE]
        #     else:
        #         allActions = [Actions.FIREUP]

        # return random.choice(legalActions)
        return action

    def isExpectimaxAgent(self) -> bool:
        '''
        Returns True if agent requires player as a variable
        :return: {bool} Returns True if player variable requires updating, otherwise false
        '''
        return True

    def take_action(self, action: Actions):
        if action in self.get_all_possible_raw_actions():
            agent_copy = self.deepcopy()
            if agent_copy.counter is not None and agent_copy.counter > 0:
                agent_copy.counter -= 1
            agent_copy.performAction(action)
            agent_copy.hasAlreadyMoved = True
            return agent_copy
        else:
            return self

    def getPointValue(self) -> int:
        return -100

    def getCount(self) -> int:
        return self.counter

    def __str__(self):
        return f"ExpectiMax at col/x = {self.get_position()[1]}\t row/y = {self.get_position()[0]},\t count: {self.counter}"