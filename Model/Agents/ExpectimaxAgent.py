import uuid
import random
from math import inf

from Model.GameState import GameState
from Model.Agents.Actions import Actions
from Model.Agents.AgentSuperClass import AgentSuperClass


class ExpectimaxAgent(AgentSuperClass):
    def __init__(self, agent_length: int = 1, agent_height: int = 1, lowest_row: int = 1, least_col: int = 1,
                 depth: int = 0, count: int = 10):
        super().__init__(agent_length, agent_height, lowest_row, least_col)
        self.counter = count
        self.id = uuid.uuid4()
        self.depth = depth
        self.currentScore = 0

    def get_all_possible_raw_actions(self) -> list:
        allactions = [Actions.STOP, Actions.UP, Actions.DOWN, Actions.LEFT, Actions.RIGHT,
                      Actions.FIRE]
        return allactions

    def isPlayer(self):
        return True

    def deepcopy(self):
        copy = ExpectimaxAgent(self.agent_length,self.agent_height, self.lowest_row, self.least_col,
                               depth=self.depth, count=self.counter)
        copy.hasAlreadyMoved = self.hasAlreadyMoved
        copy.id = self.id
        return copy

    def respawnPlayer(self):
        return ExpectimaxAgent(self.agent_length,self.agent_height,self.spawn_y, self.spawn_x, count=self.counter)

    def getDepth(self):
        return self.depth

    def autoPickAction(self, state: GameState = None) -> Actions:
        """
        Picks one of potentially many pre-defined actions randomly
        in a uniform distribution.
        :return:
        """

        # extract player agent position from state
        if state is None:
            raise ValueError("GameState cannot be None for Expectimax Agent")

        # Deep copy of agent and depth
        stateCopy = state.deepCopy()
        agentCopy = self.deepcopy()
        depth = agentCopy.getDepth()

        while depth >= 0:
            print()
            print("DEPTH", depth)
            depth -= 1

            #Get all legal actions of player, arg is 0 because player index is 0
            legalActions = stateCopy.getAllLegalActions(0)
            print("PLAYER ACTIONS: ", legalActions)
            #get current score of state
            score = stateCopy.score
            print("SCORE:", score)

            # generate a new state per legal agent actions
            actionScoreDictionary = {}
            for playerAction in legalActions:
                print()
                print("PLAYER ACTION", playerAction)
                new_state = stateCopy.generateSuccessorState(0, playerAction)
                #score of state where player agent has moved to a new position, but no enemies have moved yet
                playerScore = new_state.score
                print("PLAYER SCORE = ", playerScore)

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
            print()
            print("BEST ACTION", bestAction)

            # agentCopy.performAction(bestAction)
            #
            # new_state = stateCopy.generateSuccessorState(0, bestAction)
            # allEnemyAgentsList = new_state.current_agents[1:]
            # for eachEnemy in allEnemyAgentsList:
            #     if eachEnemy.isHeuristicAgent():
            #         eachEnemy.autoPickAction(new_state)
            #     else:
            #         eachEnemy.autoPickAction()
            #
            # print("HAVE ALL AGENTS MOVED? ", stateCopy.haveAllAgentsMoved())
            # stateCopy.moveAllProjectiles()

        # action = random.choice(legalActions)
        action = bestAction
        print()

        #if enemies are minimizer nodes, then you need to go from minimizer node -> minimizer node until all enemies have moved
        #then you can go the the next depth

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