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

        def expectiMaxFunction(state, depth, agentIndex):
            """
            get depth
            if it cycles back to player move down the tree
            """
            if (agentIndex == 0):
                nextDepth = depth - 1
            else:
                nextDepth = depth

            # print()
            # print("DEPTH", depth)
            # depth -= 1

            """
            Base or terminating case
            """
            if (nextDepth <= 0) or (state.isWin()) or (state.isLose()) or (state.isGameOver()):
                return state.score, None

            """
            max = player
            min = enemyShip
            """
            if (agentIndex == 0):
                agentType = max
                bestValue = -inf

            else:
                agentType = min
                bestValue = inf

            """
            modulo to keep reverting back and forth between ship and enemyShip
            """
            #Let's ay you have 2 enemies
            # index of player is 0 -> 0 + 1 % 3 = 1
            # if you go to enemy index = 2 -> 2 + 1 = 3 % 3 = 0
            nextAgent = (agentIndex + 1) % len(state.current_agents)

            """
            legal actions list available for an agent
            """
            # print(state.getAllLegalActions(agentIndex))
            legalActionsList = state.getAllLegalActions(agentIndex)

            """
            If agents are not player
            """
            if (agentIndex != 0):
                """
                Probability = branches of the node of possible agent moves
                """
                probability = 1.0 / len(legalActionsList)
                averageValue = 0

                """
                Loop - get all successor states and legal actions for enemy ships
                """
                # print("ENEMY AGENT: ", agentIndex)
                enemyScoreDict = {}
                for legalAction in legalActionsList:
                    successorState = state.generateSuccessorState(agentIndex, legalAction)
                    nodeValue, direction = expectiMaxFunction(successorState, nextDepth, nextAgent)
                    """
                    calculate for the average of all available nodes
                    """
                    averageValue += probability * nodeValue
                    enemyScoreDict[legalAction] = averageValue
                    # print(enemyScoreDict)

                # print("ENEMY ", agentIndex, enemyScoreDict)

                # maxVal = max(enemyScoreDict, key=enemyScoreDict.get)
                # print("ENEMY ", agentIndex, "MAXVAL", maxVal, enemyScoreDict[maxVal])
                # print(agentIndex, averageValue, legalAction)
                # print("ENEMY ", agentIndex, averageValue)

                return averageValue, legalAction


            """
            Loop - get all successor states and legal actions for pacman
            """
            # print("PLAYER AGENT: ", agentIndex)
            playerScoreDict = {}
            for legalAction in legalActionsList:
                # print("PLAYER AGENT: ", agentIndex, legalAction)
                successorState = state.generateSuccessorState(agentIndex, legalAction)
                actionValue, direction = expectiMaxFunction(successorState, nextDepth, nextAgent)
                playerScoreDict[legalAction] = actionValue

                # print(actionValue, direction)

                """
                Decide on the best course of action by getting best value
                """
                if (agentType(bestValue, actionValue) == actionValue):
                    bestValue = actionValue
                    bestAction = legalAction
                    # print(agentIndex, bestValue, bestAction)

            # print("PLAYER", agentIndex, playerScoreDict)
            maxVal = max(playerScoreDict, key=playerScoreDict.get)
            # print("PLAYER ", agentIndex, "MAXVAL", maxVal, playerScoreDict[maxVal])

            return bestValue, bestAction

        try:
            bestScore, bestAction = expectiMaxFunction(stateCopy, 2, 0)
            print("PASS: ", bestScore, bestAction)
            print()
        except IndexError:
            print("EXCEPT: ")
            print()
            return Actions.STOP

        #if enemies are minimizer nodes, then you need to go from minimizer node -> minimizer node until all enemies have moved
        #then you can go the the next depth

        # return random.choice(legalActions)
        return bestAction



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
        return 100

    def getCount(self) -> int:
        return self.counter

    def __str__(self):
        return f"ExpectiMax at col/x = {self.get_position()[1]}\t row/y = {self.get_position()[0]},\t count: {self.counter}"