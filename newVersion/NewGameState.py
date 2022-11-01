from Actions import Actions
from AgentAbstractClass import AgentAbstractClass
from AgentInterface import AgentInterface
from newVersion.GameBoard import GameBoard

class NewGameState:
    '''
    This class represents any given state during the game
    It keeps track of:
        - gameBoard
        - how many turns left until game ends
        - player lives left
        - amount of enemies on screen at any one time
        - agents
    '''
    def __init__(self,board_len: int = 10, board_height: int = 10,
                 max_enemies_at_one_time: int =1,
                 max_turn_length: int = 100, player_lives: int =1):
        '''
        Constuctor for the gameState
        :param board_len: {int} length of the board
        :param board_height: {int} height of the board
        :param max_enemies_at_one_time: {int} amount of enemies allows at any one turn
        :param max_turn_length: {int} turns until the game ends
        :param player_lives: {int} how many lives a player has
        '''
        self.turns_left = max_turn_length
        self.gameBoard = GameBoard(board_len, board_height)
        self.max_enemies_at_any_given_time = max_enemies_at_one_time
        self.current_player_lives = player_lives
        self.current_agents = []
        self.current_projectiles = []
        self.isPlayerAdded = False


    def addAgent(self, agent: AgentAbstractClass) -> bool:
        '''
        Adds an agent to the list of current agents. Player agent
        MUST be first agent added. This does not care about agent
        positions to allow for agents to come into board
        from outside the boundary
        :param agent: {Agent} adds an agent to list of current agents
        :return: {bool} True if successfully added, false otherwise
        '''

        # empty agent list
        if len(self.current_agents) == 0:
            # enforce that player agent is first element, so don't add enemies first
            if agent.isPlayer == False:
                print("WARNING: Player agent must be added first, no agent added")
                return False
            else: # adding player agent as first element
                # check if player position is valid
                if self.isValidAgent(agent):
                    self.current_agents.append(agent)
                    self.isPlayerAdded = True
                    return True
                else:
                    print(f"WARNING: Cannot place player is position ({agent.lowest_row, agent.least_col})")
                    return False

        else: # length of list > 1 i.e. player already added
            if agent.isPlayer() == True and self.isPlayerAdded == True:
                print("WARNING: Player agent already added, cannot add more player agents")
                return False
            else: # if enemy agent, check we don't add more than allowed at one state
                current_amt_enemies = len(self.current_agents) - 1
                if (current_amt_enemies < self.max_enemies_at_any_given_time):
                    # now we check that enemy doesn't spawn inside player agent
                    self.current_agents.append(agent)
                    return True
                else:
                    print("WARNING: Cannot exceed enemy agent limit, agent not added")
                    return False


    def update_board(self):
        '''
        Updates the gameBoard attribute with positions of each agent
        :return:
        '''
        pass

    def isValidAgent(self, agent: AgentInterface) -> bool:

        #TODO how to deal if agent moves to a position where another agent kills it?
        board_min_x,board_max_x, board_min_y, board_max_y = self.gameBoard.getBoardBoundaries()
        agent_min_x, agent_max_x = agent.get_row_boundaries() # x is up or down so row bounds
        agent_min_y, agent_max_y = agent.get_col_boundaries() # y is left or right so col bounds
        isAgentPlayer = agent.isPlayer()

        # if it is a player agent
        # cannot go beyond any boundaries
        if isAgentPlayer:
            if (agent_min_x < board_min_x):
                return False
            elif (agent_max_x > board_max_x):
                return False
            elif (agent_min_y < board_min_y):
                return False
            elif (agent_max_y > board_max_y):
                return False
            else:
                return True
        #enemies are allowed to go beyond left boundary (beyond board min col/y)
        # and come in from right boundary (beyond board max col/y)
        if isAgentPlayer == False:
            if agent_min_y < board_min_y:
                return False
            if agent_max_y > board_max_y:
                return False
            else:
                return True

    def getAllLegalActions(self, agentIndex: int) -> list:
        agentTakingAction: AgentInterface = self.current_agents[agentIndex]

        all_actions = agentTakingAction.get_all_possible_raw_actions()
        legal_actions = []

        for eachAction in all_actions:
            # if action is valid add it to legal actions list
            if self.isValidAgent(agentTakingAction.takeAction(eachAction)):
                legal_actions.append(eachAction)

        return legal_actions

    def generateSuccessorState(self, agentIndex: int, action: Actions):
        pass








