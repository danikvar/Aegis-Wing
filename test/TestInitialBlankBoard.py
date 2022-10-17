import unittest
from GameState import GameState
from Agent import Agent

#initialize variables
g1 = GameState()
g2 = GameState()
g2.add_player_agent(Agent())
class InitialBlankBoardTest(unittest.TestCase):

    #test default constructor values
    def test_default_constructor(self):
        self.assertEqual(10,g1.board_len)
        self.assertEqual(10, g1.board_height)
        self.assertEqual(1, g1.max_enemies_at_one_time)
        self.assertEqual(100, g1.turns_until_game_ends)
        self.assertEqual(3, g1.player_lives_left)
        self.assertEqual(5, g1.min_enemy_spawn_x_distance)


    #Case where enemy agent spawns in the same pos as player
    # assuming enemy agent and player agent have size (1,1)
    def test_min_enemy_spawn_distance_error(self):
        with self.assertRaises(ValueError):
            GameState(min_enemy_spawn_x_distance=0)

    def test_get_board_dimensions(self):
        self.assertEqual((10,10), g1.get_board_dimensions())
        self.assertEqual((5,6),
                         GameState(board_len=5,board_height=6).get_board_dimensions())


    # if no agents in gamestate
    def test_get_all_agent_error(self):
        with self.assertRaises(RuntimeError):
            g1.get_all_agents()



def main():
    unittest.main(verbosity = 3)
if __name__ == '__main__':
    main()