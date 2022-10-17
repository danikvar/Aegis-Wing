import unittest
from GameState import GameState
from Agent import PlayerAgent

#set to false to disable printing board to terminal
display = True

class TestBoardWithPlayer(unittest.TestCase):

    def setUp(self) -> None:
        self.current_game_state = GameState()

    def test_init_agent_pos(self):
        player = PlayerAgent()

        self.current_game_state.add_player_agent(player)
        agent_x = player.lowest_row
        agent_y = player.least_col

        self.current_game_state.instate_agents_to_board_initial()

        current_board = self.current_game_state.board

        #test in right position
        self.assertEquals(1, current_board[agent_x][agent_y])
        #test surrounding positions are empty
        self.assertEquals(0, current_board[agent_x + 1][agent_y])
        self.assertEquals(0, current_board[agent_x][agent_y + 1])

        if display == True:
            print("test_init_agent_pos -> line 28")
            print(self.current_game_state.get_board_as_string())

    def test_start_agent_at_diff_pos_within_boundaries(self):
        player = PlayerAgent(lowest_row=2, least_col=5)

        self.current_game_state.add_player_agent(player)

        self.current_game_state.instate_agents_to_board_initial()

        current_board = self.current_game_state.get_board()

        self.assertEquals(1,current_board[2][5])


        for i in range(4,7):
            # check row below is still 0
            self.assertEqual(0, current_board[1][i])
            # check row abow still 0
            self.assertEqual(0, current_board[3][i])

        for k in range(1,4):
            #check col to the left is 0
            self.assertEqual(0,current_board[k][4])
            #check col to the right is still 0
            self.assertEqual(0,current_board[k][6])




        if display == True:
            print("\n test_start_agent_at_diff_pos_within_boundaries -> line 43")
            print(self.current_game_state.get_board_as_string())

    def test_start_agent_bigger_len_within_boundaries(self):
        player = PlayerAgent(agent_length=3, lowest_row=2, least_col=5)
        self.current_game_state.add_player_agent(player)
        self.current_game_state.instate_agents_to_board_initial()

        current_board = self.current_game_state.get_board()

        self.assertEqual(1, current_board[2][5])
        self.assertEqual(1, current_board[2][6])
        self.assertEqual(1, current_board[2][7])

        #check surrounding is still 0
        for i in range(4,8):
            # row below is all 0
            self.assertEqual(0, current_board[1][i])

        for j in range(4,8):
            # row above all 0
            self.assertEqual(0, current_board[3][i])

        for k in range(1,4):
            # col to the left is 0
            self.assertEqual(0,current_board[k][4])

        for k in range(1,4):
            #col to the right is 0
            self.assertEqual(0,current_board[k][8])

        if display == True:
            print(self.current_game_state.get_board_as_string())

    def test_start_agent_bigger_height_within_boundaries(self):
        player = PlayerAgent(agent_height=2, lowest_row=5, least_col=7)

        self.current_game_state.add_player_agent(player)
        self.current_game_state.instate_agents_to_board_initial()

        current_board = self.current_game_state.get_board()

        self.assertEqual(1, current_board[5][7])
        self.assertEqual(1, current_board[6][7])

        # test surrounding still 0
        for i in range(4,8):
            self.assertEqual(0, current_board[i][6])
            self.assertEqual(0, current_board[i][8])

        for j in range(6,9):
            self.assertEqual(0,current_board[4][j])
            self.assertEqual(0, current_board[7][j])

        if display == True:
            print(self.current_game_state.get_board_as_string())





def main():
    unittest.main(verbosity=3)

if __name__ == "__main__":
    main()