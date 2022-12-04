import random

from Model.Agents.Actions import Actions
from Model.Agents.AgentInterface import AgentInterface
from Model.Agents.BasicCounterAgent import BasicCounterAgent
from Model.Agents.EnemyAgentBasicFireAndMove import EnemyAgentBasicFireAndMove
from Model.Agents.EnemyMoveFireHeuristicAgent import EnemyMoveFireHeuristicAgent
from Model.Agents.PlayerAgent import PlayerAgent
from Model.Agents.SimpleGoLeftAgent import SimpleGoLeftAgent
from Model.EnemyPicker import EnemyPicker
from Model.GameBoard import GameBoard
from Model.GameState import GameState

"""
This game loop will be used to train a reinforcement model
"""

########## Basic Game Configuration ##########
BOARD_ROWS = 8
BOARD_COLUMNS = 7
MAX_ENEMIES_AT_ANY_TIME = 5
GENERAL_SPAWN_RATE = 50  # represents 50% general spawn rate
TURNS_UNTIL_GAME_FINISHED = 300
PLAYER_INITIAL_SPAWN_ROW_POSITION = BOARD_ROWS // 2  # spawn in middle of board rows
PLAYER_INITIAL_SPAWN_COL_POSITION = 0  # spawn player at furthest left position
PLAYER_LIVES = 1

########## Specific Enemy Spawn Rate Configuration ##########
# if enemy does get spawned then this is the probability they get chosen
HEURISTIC_SR = 15
TURN_SPAN_SR = 20  # a.k.a counter agent
BASIC_FIRE_AND_MOVE_SR = 20
SIMPLE_GO_LEFT_SR = 45

########## Counter 'type' Enemy Configuration ##########
TURNS_UNTIL_LEAVE_BOARD = 5

########## Enemy Spawner Configuration and set up ##########
# lowest row and least col don't matter because enemy spawner will change it
HEURISTIC_AGENT = EnemyMoveFireHeuristicAgent(0, 0,count=TURNS_UNTIL_LEAVE_BOARD)
TURN_SPAN_AGENT = BasicCounterAgent(0,0,TURNS_UNTIL_LEAVE_BOARD,0,0)
BASIC_FIRE_AND_MOVE_AGENT = EnemyAgentBasicFireAndMove(0,0)
SIMPLE_GO_LEFT_AGENT = SimpleGoLeftAgent(0,0)

# ENEMY_POOL and ENEMY_SPAWN_RATES are Associative arrays, please do NOT modify these lists
ENEMY_POOL = [HEURISTIC_AGENT, TURN_SPAN_AGENT, BASIC_FIRE_AND_MOVE_AGENT, SIMPLE_GO_LEFT_AGENT]
ENEMY_SPAWN_RATES = [HEURISTIC_SR, TURN_SPAN_SR, BASIC_FIRE_AND_MOVE_SR, SIMPLE_GO_LEFT_SR]

GAMEBOARD_INFO = GameBoard(board_length=BOARD_COLUMNS, board_height=BOARD_ROWS)
ENEMY_SPAWNER = EnemyPicker(GAMEBOARD_INFO, GENERAL_SPAWN_RATE)

for i in range(len(ENEMY_POOL)):
    ENEMY_SPAWNER.add_enemy_to_spawn_list(ENEMY_POOL[i],ENEMY_SPAWN_RATES[i])

ENEMY_SPAWNER.initialize_spawn_behavior()

def print_enemies_status(gameState: GameState ):
    all_enemy_agents = gameState.current_agents[1:]

    if len(all_enemy_agents) == 0:
        print("No Enemies on board")
        return

    print(f"Total enemies on board: {len(all_enemy_agents)}")

    for each_enemy_index in range(len(all_enemy_agents)):
        print(str(each_enemy_index + 1) + ".) " + all_enemy_agents[each_enemy_index].__str__())

def print_board(gameState: GameState):
    print(f"Turns left: {gameState.turns_left}")
    print(gameState.gameBoard)

def print_score_and_status(gameState: GameState):
    if gameState.isWin():
        print("Player WON! :D")
    elif gameState.isLose():
        print("Player LOST! :( ")
    print(f"Score: {gameState.score}")

def main():

    #set to false to turn off print statements
    visualize_game = True

    starting_gamestate = GameState(board_len=BOARD_COLUMNS, board_height=BOARD_ROWS,
                                   max_enemies_at_one_time=MAX_ENEMIES_AT_ANY_TIME,
                                   turns_left=TURNS_UNTIL_GAME_FINISHED,
                                   player_lives=PLAYER_LIVES)

    # player will be of size 1 X 1
    player_agent = PlayerAgent(1, 1, PLAYER_INITIAL_SPAWN_ROW_POSITION,
                               PLAYER_INITIAL_SPAWN_COL_POSITION)

    did_add_agent = starting_gamestate.addAgent(player_agent)

    if (did_add_agent == False):
        raise RuntimeError("Could not add player agent")

    current_state = starting_gamestate

    if visualize_game:
        print("Staring GameState")
        print_board(current_state)
        print_score_and_status(current_state)
        end_line = "=" * 50
        print(end_line,"\n")

    # game loop
    while current_state.isWin() == False and current_state.isLose() == False:
        removed_counter = 0
        break_flag = False
        #have each agent take an action
        for each_index in range(0,len(current_state.current_agents)):
            if break_flag == True:
                break

            break_flag = False
            diff = None
            each_index = each_index - removed_counter
            try:
                each_agent: AgentInterface = current_state.current_agents[each_index]
            # this error only happens if an agent in the previous state was killed or removed from board
            # if agent was removed from list each_index value will be off by 1
            except IndexError:
                print(f"current index is {each_index}")
                print(f"Highest valid index is {len(current_state.current_agents) - 1}")
                diff = each_index - len(current_state.current_agents) - 1
                each_index = len(current_state.current_agents) - 1
                print(f"updated index is {each_index}")

                each_agent: AgentInterface = current_state.current_agents[each_index]

                removed_counter = diff

                if each_agent.hasMoved():
                    removed_counter += 1
                    break_flag = False
                    break # move on to next agent
                else:
                    break_flag = False
                    removed_counter += 1

            if diff != None:
                print(f"updated index is {each_index}")

            if each_agent.isPlayer():
                #TODO DAN YOU WILL HAVE TO MAKE YOUR OWN PLAYER AGENT CLASS and overwrite auto pick action
                DEFAULT_ACTION = Actions.STOP
                agent_action = DEFAULT_ACTION

            elif each_agent.isHeuristicAgent():
                agent_action = each_agent.autoPickAction(current_state)
            else:
                agent_action = each_agent.autoPickAction()

            current_state = current_state.generateSuccessorState(each_index, agent_action)

        #once all agents have taken an action decrement the turn
        current_state.decrement_turn()
        # Reset move status of agents after everyone has moved
        current_state.reset_agents_move_status()

        # spawn enemies at the start of new turn
        if len(current_state.current_agents) - 1 < current_state.max_enemies_at_any_given_time:
            # spawn enemy based on spawn rate
            probability_to_spawn = random.randint(0, 100)
            if probability_to_spawn <= ENEMY_SPAWNER.spawn_rate:
                # pick an enemy
                enemy_to_spawn = ENEMY_SPAWNER.choose_enemy()
                current_state.addAgent(enemy_to_spawn)

        #Optional board visualization
        if visualize_game:
            print_enemies_status(current_state)
            print_board(current_state)
            print_score_and_status(current_state)
            print(end_line)


if __name__ == "__main__":
    main()
