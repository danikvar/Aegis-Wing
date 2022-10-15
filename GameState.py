from Agent import Agent
class GameState():

    def __init__(
            self,board_len = 10, board_height = 10, max_enemies_at_one_time=1,
            max_turn_length=100, player_lives=3):
        self.board_len = board_len
        self.board_height = board_height
        self.max_enemies_at_one_time = max_enemies_at_one_time
        self.turns_until_game_ends = max_turn_length
        self.current_turn = max_turn_length
        self.player_lives_left = player_lives
        self.board = self.initialize_board()
        self.agent_list = []

    # set up board
    def initialize_board(self) -> list:
        board_2d_array = []
        for i in range(0,self.board_len):
            any_row = []
            for j in range(0,self.board_height):
                any_row.append(0)
            board_2d_array.append(any_row)

        return board_2d_array


    def get_board_dimensions(self) -> tuple:
        return (self.board_len,self.board_height)

    def add_player_agent(self, agent: Agent) -> bool:
        '''
        Adds a player agent to a list of agents. Player must be the first
        element added to maintain make sure get_player_agent_function actually
        returns the correct agent
        :param agent: {Agent} The player agent instance
        :return: {bool} true if the player was successfully added, false otherwise
        '''
        if len(self.agent_list) != 0:
            return False
        else:
            player_agent = Agent(agent.agent_len_x,agent.agent_len_y,agent.pos_x,agent.pos_y)
            self.agent_list.append(player_agent)
            return True

    def get_player_agent(self) -> Agent:
        #force agent player to be first index value in list
        return self.agent_list[0]

    def add_enemy_agent(self, agent: Agent):
        '''
        Adds an enemy agent to a list of agents.
        Player agent must already have been added otherwise this will fail
        :param agent: {Agent} The enemy agent instance
        :return: {bool} true if the enemy was successfully added, false otherwise
        '''
        #player agent must be added first to keep integrity of index
        if len(self.agent_list) < 1:
            return False
        player = self.get_player_agent()
        # enemy cannot overlap player and should probably start off
        # at minimum like 5 spaces away to the right on the x axis

        #furthest most right part of the ship
        min_x_dist_to_spawn = player.pos_x + 5

        if agent.get_min_x_boundary() < min_x_dist_to_spawn:
            return False
        else:
            self.agent_list.append(agent)
            return True


