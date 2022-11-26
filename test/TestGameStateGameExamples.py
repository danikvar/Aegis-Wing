import random
import unittest

from Model.Agents.Actions import Actions
from Model.Agents.AgentInterface import AgentInterface
from Model.Agents.EnemyAgentBasicFireAndMove import EnemyAgentBasicFireAndMove
from Model.Agents.PlayerAgent import PlayerAgent
from Model.Agents.SimpleGoLeftAgent import SimpleGoLeftAgent
from Model.EnemyPicker import EnemyPicker
from Model.GameState import GameState
#branch_2

class TestGameStateGameExamples(unittest.TestCase):
    def setUp(self) -> None:
        """
        Ramzi Branch 2
        Sets up variables to use. These variables are
        reset prior to every test
        :return: None
        """
        self.gamestateInit = GameState()

    def test_game_example_1(self):
        """
        Ramzi Branch 2
        In this example game loop there are 2 GO left enemies, they move at the same rate
        They do not hit the player agent
        They both exit the board simultaneously
        The game lasts for 10 turns
        :return:
        """
        # set to true to print board to terminal/console for visual aid
        print_board = True

        state = self.gamestateInit
        state.max_enemies_at_any_given_time = 2
        # set small turns
        state.turns_left = 10
        # make a player and add it
        player = PlayerAgent(1, 1, 0, 0)
        state.addAgent(player)

        enemy_1 = SimpleGoLeftAgent(9, 9)
        enemy_2 = SimpleGoLeftAgent(1, 9)

        # add agents
        state.addAgent(enemy_1)
        state.addAgent(enemy_2)

        state.update_board()

        # while game is still going
        while True:
            # get enemy agent action,
            for each_index in range(len(state.current_agents)):
                try:
                    each_agent: AgentInterface = state.current_agents[each_index]
                except IndexError:
                    # means list was shortened because enemy agent died or exited board
                    # 3 cases
                    # case 1 agent in middle of list disappeared
                    each_agent: AgentInterface = state.current_agents[each_index - 1]
                    # case agent at end of list died/disappeared
                    # no more agents to move
                    if each_agent.hasMoved():
                        state.decrement_turn()
                        break
                    else:
                        each_index -= 1
                    # continue otherwise
#TODO check if agent is heuristic if so pass state intp autopickaction, have autopick action take null param by default
                # making player action just stop for this example
                if each_agent.isPlayer():
                    agent_action = Actions.STOP
                else:
                    agent_action = each_agent.autoPickAction()

                # len of current agents may change here, potentiall causing index error
                state = state.generateSuccessorState(each_index, agent_action)

                if (state.current_agents[len(state.current_agents) - 1].hasMoved() == True):
                    state.decrement_turn()

                    if print_board:
                        print("Turn: " + str(state.turns_left))
                        print(state.gameBoard)
                        print(f"lives left: {state.current_player_lives}")
                        print(f"Win?\t{state.isWin()}\nLose?\t{state.isLose()}\n")
            # once for loop is done reset move status
            state.reset_agents_move_status()

            if state.isWin() or state.isLose():
                break

        self.assertEquals(1, state.gameBoard.board_array[0][0])

    def test_game_example_2(self):
        """
        Ramzi Branch 2
        For this test
            - 2 enemies
            - neither enemy hits player
            - one enemy exits the game before the other
        :return:
        """
        # set to true to print board to terminal/console for visual aid
        print_board = True

        state = self.gamestateInit
        state.max_enemies_at_any_given_time = 2
        # set small turns
        state.turns_left = 10
        # make a player and add it
        player = PlayerAgent(1, 1, 0, 0)
        state.addAgent(player)


        enemy_1 = SimpleGoLeftAgent(9, 9)
        #row 1, col = 7
        enemy_2 = SimpleGoLeftAgent(1, 7)

        # add agents
        state.addAgent(enemy_1)
        state.addAgent(enemy_2)

        state.update_board()

        # while game is still going
        while True:
            # get enemy agent action,
            for each_index in range(len(state.current_agents)):
                try:
                    each_agent: AgentInterface = state.current_agents[each_index]
                except IndexError:
                    # means list was shortened because enemy agent died or exited board
                    # 3 cases
                    # case 1 agent in middle of list disappeared
                    each_agent: AgentInterface = state.current_agents[each_index - 1]
                    # case agent at end of list died/disappeared
                    # no more agents to move
                    if each_agent.hasMoved():
                        state.decrement_turn()
                        break
                    else:
                        each_index -= 1
                    # continue otherwise

                # making player action just stop for this example
                if each_agent.isPlayer():
                    agent_action = Actions.STOP
                else:
                    agent_action = each_agent.autoPickAction()

                # len of current agents may change here, potentiall causing index error
                state = state.generateSuccessorState(each_index, agent_action)

                if (state.current_agents[len(state.current_agents) - 1].hasMoved() == True):
                    state.decrement_turn()

                    if print_board:
                        print("Turn: " + str(state.turns_left))
                        print(state.gameBoard)
                        print(f"lives left: {state.current_player_lives}")
                        print(f"Win?\t{state.isWin()}\nLose?\t{state.isLose()}\n")
            state.reset_agents_move_status()

            if state.isWin() or state.isLose():
                break

        self.assertEquals(1, state.gameBoard.board_array[0][0])

    def test_game_example_3(self):
        """
        Ramzi Branch 2
        For this test
            - 2 enemies
            - One enemy hits player, causes player to lose
        :return:
        """

        # set to true to print board to terminal/console for visual aid
        print_board = True

        state = self.gamestateInit
        state.max_enemies_at_any_given_time = 2
        # set small turns
        state.turns_left = 10
        # make a player and add it
        player = PlayerAgent(1, 1, 0, 0)
        state.addAgent(player)

        enemy_1 = SimpleGoLeftAgent(9, 9)
        # row 1, col = 7
        enemy_2 = SimpleGoLeftAgent(0, 5)

        # add agents
        state.addAgent(enemy_1)
        state.addAgent(enemy_2)

        state.update_board()

        # while game is still going
        while True:
            # get enemy agent action,
            for each_index in range(len(state.current_agents)):
                try:
                    each_agent: AgentInterface = state.current_agents[each_index]
                except IndexError:
                    # means list was shortened because enemy agent died or exited board
                    # 3 cases
                    # case 1 agent in middle of list disappeared
                    each_agent: AgentInterface = state.current_agents[each_index - 1]
                    # case agent at end of list died/disappeared
                    # no more agents to move
                    if each_agent.hasMoved():
                        state.decrement_turn()
                        break
                    else:
                        each_index -= 1
                    # continue otherwise

                # making player action just stop for this example
                if each_agent.isPlayer():
                    agent_action = Actions.STOP
                else:
                    agent_action = each_agent.autoPickAction()

                # len of current agents may change here, potentiall causing index error
                state = state.generateSuccessorState(each_index, agent_action)

                if (state.current_agents[len(state.current_agents) - 1].hasMoved() == True):
                    state.decrement_turn()

                    if print_board:
                        state.update_board()
                        print("Turn: " + str(state.turns_left))
                        print(state.gameBoard)
                        print(f"lives left: {state.current_player_lives}")
                        print(f"Win?\t{state.isWin()}\nLose?\t{state.isLose()}\n")

            state.reset_agents_move_status()

            if state.isWin() or state.isLose():
                break

        self.assertEquals(0, state.gameBoard.board_array[0][0])

    def test_game_example_4(self):
        """
        Ramzi Branch 3
        Game Conditions:
        - 10 turns player spawn in middle of board on furthest left col
        - Spawn rate is 100%
        - max enemies is 5
        - Only enemy type is SimpleGoLeft
        - 1 enemy should spawn per turn up until turn 5, total 5 enemies
        - player will not move the whole time
        - score should be 5
        :return:
        """

        # set to true to print board to terminal/console for visual aid
        print_board = True

        state = self.gamestateInit
        state.max_enemies_at_any_given_time = 5
        # set small turns
        state.turns_left = 10
        # make a player size 1 X 1 at row=5,col=0 and add it
        player = PlayerAgent(1, 1, 5, 0)
        state.addAgent(player)

        #pass in gameboard to get spawn boundaries, 2nd param is spawn rate
        enemy_spawner = EnemyPicker(state.gameBoard, 100)
        enemy_spawner.add_enemy_to_spawn_list(SimpleGoLeftAgent(1,1),15) #weight doesn't mattter if only one enemy type to spawn
        enemy_spawner.initialize_spawn_behavior()
        state.update_board()

        PLAYER_ACTION = Actions.STOP #placeholder action

        #Main game loop
        while state.turns_left > 4:
            # move each agents
            for each_index in range(len(state.current_agents)):
                try:
                    each_agent: AgentInterface = state.current_agents[each_index]
                except IndexError:
                    # means list was shortened because enemy agent died or exited board
                    # 3 cases
                    # case 1 agent in middle of list disappeared
                    each_agent: AgentInterface = state.current_agents[each_index - 1]
                    # case agent at end of list died/disappeared
                    # no more agents to move
                    if each_agent.hasMoved():
                        state.decrement_turn()
                        break
                    else:
                        each_index -= 1
                    # continue otherwise

                # making player action just stop for this example
                if each_agent.isPlayer():
                    agent_action = PLAYER_ACTION
                else:
                    agent_action = each_agent.autoPickAction()

                # len of current agents may change here, potentiall causing index error
                state = state.generateSuccessorState(each_index, agent_action)

                if (state.current_agents[len(state.current_agents) - 1].hasMoved() == True):
                    state.decrement_turn()
                    # spawn enemy based on spawn rate
                    #pick random number
                    probability_to_spawn = random.randint(0,100)
                    if probability_to_spawn <= enemy_spawner.spawn_rate:
                        #pick an enemy
                        enemy_to_spawn = enemy_spawner.choose_enemy()
                        state.addAgent(enemy_to_spawn)

                    if print_board:
                        print("Turn: " + str(state.turns_left))
                        print(state.gameBoard)
                        print(f"lives left: {state.current_player_lives}")
                        print(f"Win?\t{state.isWin()}\nLose?\t{state.isLose()}\n")

            state.reset_agents_move_status()

        self.assertEquals(6, len(state.current_agents))

    def test_game_example_5(self):
        """
        Ramzi Branch 3
        - 10 turns player spawn in middle of board on furthest left col
        - Spawn rate is 100%
        - max enemies is 5
        - 2 enemy types SimpleGoLeft and EnemyAgentBasicFireAndMove
        - 1 enemy should spawn per turn up until turn 5, total 5 enemies
        - player will not move the whole time
        - score should be 5
        :return:
        """

        # set to true to print board to terminal/console for visual aid
        print_board = True

        state = self.gamestateInit
        state.max_enemies_at_any_given_time = 5
        # set small turns
        state.turns_left = 10
        # make a player size 1 X 1 at row=5,col=0 and add it
        player = PlayerAgent(1, 1, 5, 0)
        state.addAgent(player)

        # pass in gameboard to get spawn boundaries, 2nd param is spawn rate
        enemy_spawner = EnemyPicker(state.gameBoard, 100)
        enemy_spawner.add_enemy_to_spawn_list(SimpleGoLeftAgent(1, 1),
                                              50)  # pos doesn't matter it will be changed by spawner
        enemy_spawner.add_enemy_to_spawn_list(EnemyAgentBasicFireAndMove(1,1),
                                              50)
        #now 50/50 chance that enemy will be a Simple Go Left or an EnemyAgentBasicFireAndMove
        enemy_spawner.initialize_spawn_behavior()
        state.update_board()

        PLAYER_ACTION = Actions.STOP  # placeholder action

        # Main game loop
        while state.turns_left > 4:
            # move each agents
            for each_index in range(len(state.current_agents)):
                try:
                    each_agent: AgentInterface = state.current_agents[each_index]
                except IndexError:
                    # means list was shortened because enemy agent died or exited board
                    # 3 cases
                    # case 1 agent in middle of list disappeared
                    each_agent: AgentInterface = state.current_agents[each_index - 1]
                    # case agent at end of list died/disappeared
                    # no more agents to move
                    if each_agent.hasMoved():
                        state.decrement_turn()
                        break
                    else:
                        each_index -= 1
                    # continue otherwise

                # making player action just stop for this example
                if each_agent.isPlayer():
                    agent_action = PLAYER_ACTION
                else:
                    agent_action = each_agent.autoPickAction()

                # len of current agents may change here, potentiall causing index error
                state = state.generateSuccessorState(each_index, agent_action)

                if (state.current_agents[len(state.current_agents) - 1].hasMoved() == True):
                    state.decrement_turn()
                    if len(state.current_agents) - 1 < state.max_enemies_at_any_given_time:
                        # spawn enemy based on spawn rate
                        # pick random number
                        probability_to_spawn = random.randint(0, 100)
                        if probability_to_spawn <= enemy_spawner.spawn_rate:
                            # pick an enemy
                            enemy_to_spawn = enemy_spawner.choose_enemy()
                            state.addAgent(enemy_to_spawn)

                    if print_board:
                        state.update_board()
                        print("Turn: " + str(state.turns_left))
                        print("# Enemies on board: ", len(state.current_agents) - 1)
                        print("enemy positions: ")
                        for each in state.current_agents:
                            each_agent : AgentInterface = each
                            if each_agent.isPlayer() == False:
                                print(f"x = {each_agent.get_min_col_boundary()}, y = {each_agent.get_min_row_boundary()}, type: {type(each_agent)}")
                        print("# Projectiles on board: ", len(state.current_projectiles))
                        print(state.gameBoard)
                        print(f"lives left: {state.current_player_lives}")
                        print(f"Win?\t{state.isWin()}\nLose?\t{state.isLose()}\n")

            state.reset_agents_move_status()

        self.assertEquals(6, len(state.current_agents))



#ramzi merged
def main():
    unittest.main(verbosity=3)

if __name__ == '__main__':
    main()