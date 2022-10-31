from Agent import Agent
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


    def addAgent(self, agent: Agent) -> bool:
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
                self.current_agents.append(agent)
                self.isPlayerAdded = True
                return True

        else: # length of list > 1 i.e. player already added
            if agent.isPlayer == True and self.isPlayerAdded == True:
                print("WARNING: Player agent already added, cannot add more player agents")
                return False
            else: # if enemy agent, check we don't add more than allowed at one state
                current_amt_enemies = len(self.current_agents) - 1
                if (current_amt_enemies < self.max_enemies_at_any_given_time):
                    self.current_agents.append(agent)
                    return True
                else:
                    print("WARNING: Cannot exceed enemy agent limit, agent not added")
                    return False





