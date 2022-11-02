from Model.Agents.Actions import Actions
from Model.Agents.AgentInterface import AgentInterface
from Model.Agents.AgentSuperClass import AgentSuperClass
from Model.Agents.PlayerAgent import PlayerAgent
from Model.GameBoard import GameBoard

class GameState:
    '''
    This class represents any given state during the game
    It keeps track of:
        - gameBoard
        - how many turns left until game ends
        - player lives left
        - amount of enemies on screen at any one time
        - agents
    '''
    def __init__(self, board_len: int = 10, board_height: int = 10,
                 max_enemies_at_one_time: int =1,
                 turns_left: int = 100, player_lives: int = 1):
        '''
        Constuctor for the gameState
        :param board_len: {int} length of the board
        :param board_height: {int} height of the board
        :param max_enemies_at_one_time: {int} amount of enemies allows at any one turn
        :param turns_left: {int} turns until the game ends
        :param player_lives: {int} how many lives a player has
        '''
        self.turns_left = turns_left
        self.gameBoard = GameBoard(board_len, board_height)
        self.max_enemies_at_any_given_time = max_enemies_at_one_time
        self.current_player_lives = player_lives
        self.current_agents = [] #list of AgentInterface Objects
        self.bullet_agents = []
        self.current_projectiles = []
        self.isPlayerAdded = False


    def addAgent(self, agent: AgentSuperClass) -> bool:
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

    def decrement_turn(self):
        self.turns_left -= 1

    def set_turn(self, turns_left: int) -> None:
        if turns_left < 0:
            raise ValueError("turns_left cannot be less than 0")
        self.turns_left = turns_left

    def isWin(self) -> bool:
        #you win game if player still has lives and timer has reached 0
        if self.current_player_lives > 0 and self.turns_left == 0:
            return True
        return False

    def isGameOver(self) -> bool:
        if self.current_player_lives == 0:
            return True
        else:
            return False

    def checkPlayerAgentClashes(self):
        """
        Checks for if player clashes with enemy agents and adjusts
        hp of objects accordingly
        Enemies allowed to overlap with each other.
        Call in generateSuccessor
        :return: {None}
        """
        # agent crashing logic, check if player is overlapping with enemy agents
        player_agent: AgentInterface = self.current_agents[0]
        list_enemy_agents = self.current_agents[1:]

        for i in range(len(list_enemy_agents)):
            enemy_agent: AgentInterface = list_enemy_agents[i]

            # if overlapping, player and agent lose health
            #TODO maybe just have them blow up instead of subtracting health? Already happens since player hp = 1
            if (player_agent.is_overlapping_other_agent(enemy_agent)):
                player_agent.set_hp(player_agent.get_hp() - 1)
                enemy_agent.set_hp(enemy_agent.get_hp() - 1)

    def updateAgentsList(self):
        """
        update the agents list. If player health = 0, remove them
        If enemy agent health = 0 remove them
        If enemy agent_max_col < board_col_min remove them.
        Call this in generateSuccessor
        :return: {None}
        """
        board_min_col = self.gameBoard.min_col
        agent_indexes_to_be_popped = []

        for i in range(len(self.current_agents)):
            already_popped = False
            each_agent: AgentInterface = self.current_agents[i]
            # check if agent is dead
            if each_agent.is_dead() == True:
                # add agent index to list to be popped
                agent_indexes_to_be_popped.append(i)
                already_popped = True

            if already_popped == True:
                # will go to next agent if agent is dead
                continue
            else:
                # if enemy max col beyond board min boundary,
                # don't need to check for player because state.getAllLegalActions(0) will tell you
                # this already
                if each_agent.get_max_col_boundary() < board_min_col:
                    agent_indexes_to_be_popped.append(i)

        subtract_by = 0

        for each_index in agent_indexes_to_be_popped:
            value_to_pop = each_index - subtract_by
            current_agent: AgentInterface = self.current_agents[value_to_pop]
            # if player agent died
            if current_agent.isPlayer() == True:
                if (current_agent.is_dead()):
                    self.current_player_lives -= 1
                    if self.current_player_lives > 0:
                        self.isPlayerAdded = False
                        # if more lives left than player agent gets restarted at initial point
                        #player should always be first index i.e. 0
                        player: PlayerAgent = self.current_agents[0]
                        self.current_agents[0] = player.respawnPlayer()
                        continue

            if value_to_pop == 0:
                self.current_agents.pop(value_to_pop)
                subtract_by = 1
            else:
                value_to_pop = each_index - subtract_by
                self.current_agents.pop(value_to_pop)
                subtract_by = each_index

    def update_board(self):
        '''
        Updates the gameBoard attribute with positions of each agent.
        Call this method after calling
        - checkPlayerAgentClashes
        - updateAgentsList
        :return:
        '''
        #TODO update with bullet logic

        self.gameBoard.setUpBlankBoard()

        for i in range(len(self.current_agents)):
            self.gameBoard.populate_board(i + 1, self.current_agents[i])


    def isValidAgent(self, agent: AgentInterface) -> bool:
        """
        Helper method to getAllLegalActions and addAgent. Checks if
        the agent position is valid within the board.
        :param agent: {AgentInterface}
        :return: {bool} True if agent position is valid, false otherwise
        """

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
            if agent_min_x < board_min_x:
                return False
            if agent_max_x > board_max_x:
                return False
            else:
                return True

    def getAllLegalActions(self, agentIndex: int) -> list:
        """
        Gets all legals actions of an agent at agentIndex
        :param agentIndex: {int} index of agent in agent list
        :return: {list} a list of legal actions an agent can perform
        """
        agentTakingAction: AgentInterface = self.current_agents[agentIndex]

        all_actions = agentTakingAction.get_all_possible_raw_actions()
        legal_actions = []

        for eachAction in all_actions:
            # if action is valid add it to legal actions list
            if self.isValidAgent(agentTakingAction.take_action(eachAction)):
                legal_actions.append(eachAction)

        return legal_actions


    def generateSuccessorState(self, agentIndex: int, action: Actions):
        #TODO should this return a deepcopy of gamestate or can it reuse same state?
        # TODO does this need an already moved dict? To check if an agent has already moved?
        current_agent: AgentInterface = self.current_agents[agentIndex]
        all_legal_agent_actions = self.getAllLegalActions(agentIndex)

        if action in all_legal_agent_actions:
            self.current_agents[agentIndex] = current_agent.take_action(action)

        #after action check if player has clashed with any enemy agents
        self.checkPlayerAgentClashes()
        # update the list to reflect any clashes
        self.updateAgentsList()
        #update the board representation
        self.update_board()

        return self








