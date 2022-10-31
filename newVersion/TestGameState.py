import unittest

from newVersion.NewGameState import NewGameState
from Agent import PlayerAgent


class TestGameState(unittest.TestCase):
    def setUp(self) -> None:
        self.gamestateInit = NewGameState()
        self.gameState_2 = NewGameState()
        player = PlayerAgent()
        self.gameState_2.addAgent(player)

    # test default values
    def test_default_values(self) -> None:
        g = self.gamestateInit
        self.assertEquals(0,len(g.current_agents))
        self.assertFalse(g.isPlayerAdded)
        self.assertEquals(100, g.turns_left)
        self.assertEquals(1, g.max_enemies_at_any_given_time)

    #player added at setup
    def test_added_player(self) -> None:
        self.assertTrue(self.gameState_2.isPlayerAdded)
        self.assertEquals(1, len(self.gameState_2.current_agents))

    # should not be able to add a second player agent
    def test_adding_2_players(self):
        player_2 = PlayerAgent()
        self.assertFalse(self.gameState_2.addAgent(player_2))
        self.assertEquals(1,len(self.gameState_2.current_agents) )



def main():
    unittest.main(verbosity=3)

if __name__ == '__main__':
    main()