import unittest
from GameState import GameState
from Agent import Agent

current_game_state = GameState()
player = Agent()

#set to false to disable printing board to terminal
display = True

class TestBoardWithPlayer(unittest.TestCase):

    def test_init_agent_pos(self):
        current_game_state.add_player_agent(player)
        agent_x = player.pos_x
        agent_y = player.pos_y

        current_game_state.instate_agents_to_board_initial()

        current_board = current_game_state.board

        #test in right position
        self.assertEquals(1, current_board[agent_x][agent_y])
        #test surrounding positions are empty
        self.assertEquals(0, current_board[agent_x + 1][agent_y + 1])

        if display == True:
            print("test_init_agent_pos -> line 28")
            print(current_game_state.get_board_as_string())

    def test_start_agent_at_diff_pos_within_boundaries(self):
        player = Agent(pos_x=2,pos_y=5)

        current_game_state.add_player_agent(player)

        current_game_state.instate_agents_to_board_initial()

        print(current_game_state.get_board_as_string())

        current_board = current_game_state.board
        print(current_board)

        self.assertEquals(1, current_board[2][5])

        if display == True:
            print("\n test_start_agent_at_diff_pos_within_boundaries")
            print(current_game_state.get_board_as_string())



def main():
    unittest.main(verbosity=3)

if __name__ == "__main__":
    main()