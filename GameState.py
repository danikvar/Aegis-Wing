from Agent import Agent


class GameState:

    def __init__(
            self,board_len: int = 10, board_height: int = 10, max_enemies_at_one_time: int =1,
            max_turn_length: int = 100, player_lives: int =3, min_enemy_spawn_x_distance: int = 5):

        if min_enemy_spawn_x_distance < 1:
            error_context = f'argument min_enemy_spawn_x_distance: {min_enemy_spawn_x_distance} cannot be less than 1'
            raise ValueError(error_context)

        self.board_len = board_len
        self.board_height = board_height
        self.max_enemies_at_one_time = max_enemies_at_one_time
        self.turns_until_game_ends = max_turn_length
        self.current_turn = max_turn_length
        self.player_lives_left = player_lives
        self.board = self.initialize_board()
        self.agent_list = []
        self.min_enemy_spawn_x_distance = min_enemy_spawn_x_distance

    # set up board
    def initialize_board(self) -> list:
        board_2d_array = []
        for i in range(0,self.board_len):
            any_row = []
            for j in range(0,self.board_height):
                any_row.append(0)
            board_2d_array.append(any_row)

        return board_2d_array


    #NO logic for being outside of board, enemies shoudl be able to
    # board should not
    def instate_agents_to_board_initial(self) -> None:
        if len(self.agent_list) < 1:
            raise RuntimeError("Gamestate does not have any agents to instate on board")

        #if len(self.agent_list) == 1:
            #raise RuntimeWarning("Gamestate ONLY has a player agent")

        temp_board = self.initialize_board()

        for agent_index in range (0,len(self.agent_list)):
            # agent index needed to update board
            each_agent = self.agent_list[agent_index]

            agent_min_x = each_agent.get_min_col_boundary()
            agent_max_x = each_agent.get_max_col_boundary()
            agent_min_y = each_agent.get_min_row_boundary()
            agent_max_y = each_agent.get_max_row_boundary()

            for row_index in range(len(self.board)):
                current_row = temp_board[row_index]
                if row_index >= agent_min_y and row_index <= agent_max_y:
                    for col_index in range(len(current_row)):
                        if col_index >= agent_min_x and col_index <= agent_max_x:
                            temp_board[row_index][col_index] = agent_index + 1



        #update board
        self.board = temp_board

    def get_board(self):
        return self.board




    def get_board_dimensions(self) -> tuple:
        return (self.board_len,self.board_height)

    def get_all_agents(self) -> list:
        if len(self.agent_list) < 1:
            raise RuntimeError("No agents in gamestate, please add agents before calling get_all_agents ")

        if len(self.agent_list) == 1:
            raise RuntimeWarning("Player agent is the only agent in the gamestate")
        return self.agent_list

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
            player_agent = Agent(agent.agent_length, agent.agent_height, agent.lowest_row, agent.least_col)
            self.agent_list.append(player_agent)
            return True

    def get_player_agent(self) -> Agent:
        if len(self.agent_list) < 1:
            raise RuntimeError('Gamestate does not have a player agent,'
                               'add_player_agent first then run again')
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
        min_x_dist_to_spawn = player.lowest_row + self.min_enemy_spawn_x_distance

        if agent.get_min_col_boundary() < min_x_dist_to_spawn:
            return False
        else:
            self.agent_list.append(agent)
            return True

    def get_board_as_string(self):

        list_row_str = []

        board_str = ""


        for row in range(len(self.board)):
            temp = "|"
            temp += "\u0332" + " "
            current_row_list = self.board[row]
            for col in range(len(current_row_list)):
                temp += "\u0332" + (str(current_row_list[col]))
                temp += "\u0332" + " "
                temp += "|"
                if col < len(current_row_list) - 1:
                    temp += "\u0332" + " "
                else:
                    list_row_str.append(temp)

        for i in range(-1, -len(list_row_str) - 1, -1):
            board_str += list_row_str[i] + "\n"

        return board_str

    # def get_successor_state(self, agent_index: int, agent_action):



