import numpy as np
import gym
from gym import spaces
import matplotlib.pyplot as plt
from Model.GameState import GameState
from Model.GameBoard import GameBoard


class GameEnv(gym.Env):
    """
    Custom Environment for Stable Baseline 3 for the classic Snake
    """
    metadata = {'render.modes': ['console', 'rgb_array']}
    # Direction constants
    n_actions = 3  # 3 possible steps each turn
    LEFT = 0
    STRAIGHT = 1
    RIGHT = 2
    # Grid label constants
    EMPTY = 0
    SNAKE = 1
    WALL = 2
    FOOD = 3
    # Rewards
    # REWARD_PER_STEP = 0 # reward for every step taken, gets into infinite loops if >0
    # Define Max steps to avoid infinite loops
    REWARD_BULLET_PATH = -50  # do not want player ending 2 or < spaces away from any bullet since they will lose hp
    REWARD_NEAR_BULLET = -10  # Check how many possible future paths collide with bullet and assign -10 for each
    REWARD_WIN = 10000 # reward winning the game
    REWARD_LOSE = -1000
    REWARD_LOSE_LIFE = -100
    REWARD_TURN = 5

    def __init__(self, myState:GameState, grid_cols=12, grid_rows=12):
        super(GameEnv, self).__init__()
        # Steps so far
        self.gameState = myState
        self.stepNum = 0
        self.last_food_step = 0
        # Size of the 2D grid (including walls)
        self.grid_rows = grid_rows
        self.grid_cols = grid_cols
        # Get the player position
        self.player_coord = self.gameState.getPlayerPos()
        # Init the grid
        self.grid = self.gameState.gameBoard.board_array # set the grid to the current game gird
        #Track the number of enemies on the board
        self.numEnemies = len(self.gameState.current_agents) - 1
        # Init distance to food
        self.head_dist_to_food = self.grid_distance(self.snake_coordinates[-1], np.argwhere(self.grid == self.FOOD)[0])
        # Store init values
        self.init_grid = self.grid.copy()
        self.init_snake_coordinates = self.snake_coordinates.copy()

        # The action space
        self.action_space = spaces.Discrete(self.n_actions)
        # The observation space, "position" is the coordinates of the head; "direction" is which way the sanke is heading, "grid" contains the full grid info
        # TODO: CHANGE  THE HIGH VALUE AND IMPLEMENT A TIME STEP
        self.observation_space = gym.spaces.Dict(
            spaces={
                "position": gym.spaces.Box((0, 0), (grid_cols, grid_rows), shape=(2,)),
                "num_next_legal_dir": gym.spaces.Box(0, 4),
                "num_Enemies": gym.spaces.Box(0, self.gameState.max_enemies_at_any_given_time),
                "bullets_in_range":gym.spaces.Box(0, 11),
                "grid": gym.spaces.Box(low=0, high=3, shape=(self.grid_cols, self.grid_rows), dtype=np.uint8),
            })

    def grid_distance(self, pos1, pos2):
        return np.linalg.norm(np.array(pos1, dtype=np.float32) - np.array(pos2, dtype=np.float32))

    def reset(self):
        # Reset to initial positions
        self.stepNum = 0;
        self.last_food_step = 0
        self.grid = self.init_grid.copy()
        self.snake_coordinates = self.init_snake_coordinates.copy()
        # Init distance to food
        self.head_dist_to_food = self.grid_distance(self.snake_coordinates[-1], np.argwhere(self.grid == self.FOOD)[0])
        return self._get_obs()

    def _get_obs(self):
        direction = np.array(self.snake_coordinates[-1]) - np.array(self.snake_coordinates[-2])
        # return observation in the format of self.observation_space
        return {"position": np.array(self.snake_coordinates[-1], dtype=np.int32),
                "direction": direction.astype(np.int32),
                "grid": self.grid}

    def step(self, action):
        # Get direction for snake
        direction = np.array(self.snake_coordinates[-1]) - np.array(self.snake_coordinates[-2])
        if action == self.STRAIGHT:
            step = direction  # step in the firection the snake faces
        elif action == self.RIGHT:
            step = np.array([direction[1], -direction[0]])  # turn right
        elif action == self.LEFT:
            step = np.array([-direction[1], direction[0]])  # turn left
        else:
            raise ValueError("Action=%d is not part of the action space" % (action))
        # New head coordinate
        new_coord = (np.array(self.snake_coordinates[-1]) + step).astype(np.int32)
        # grow snake
        self.snake_coordinates.append((new_coord[0], new_coord[1]))  # convert to tuple so we can use it to index

        # Check what is at the new position
        new_pos = self.snake_coordinates[-1]
        new_pos_type = self.grid[new_pos]
        self.grid[new_pos] = self.SNAKE  # this position is now occupied by the snake
        done = False;
        reward = 0  # by default the game goes on and no reward
        if new_pos_type == self.FOOD:
            reward += self.REWARD_PER_FOOD
            self.last_food_step = self.stepNum
            # Put down a new food item
            empty_tiles = np.argwhere(self.grid == self.EMPTY)
            if len(empty_tiles):
                new_food_pos = empty_tiles[np.random.randint(0, len(empty_tiles))]
                self.grid[new_food_pos[0], new_food_pos[1]] = self.FOOD
            else:
                done = True  # no more tiles to put the food to
        else:
            # If no food was eaten we remove the end of the snake (i.e., moving not growing)
            self.grid[self.snake_coordinates[0]] = self.EMPTY
            self.snake_coordinates = self.snake_coordinates[1:]
            if (new_pos_type == self.WALL) or (new_pos_type == self.SNAKE):
                done = True  # stop if we hit the wall or the snake
                reward += self.REWARD_WALL_HIT  # penalty for hitting walls/tail
        #             else:
        #                 reward += self.REWARD_PER_STEP

        # Update distance to food and reward if closer
        head_dist_to_food_prev = self.head_dist_to_food
        self.head_dist_to_food = self.grid_distance(self.snake_coordinates[-1], np.argwhere(self.grid == self.FOOD)[0])
        if head_dist_to_food_prev > self.head_dist_to_food:
            reward += self.REWARD_PER_STEP_TOWARDS_FOOD  # reward for getting closer to food
        elif head_dist_to_food_prev < self.head_dist_to_food:
            reward -= self.REWARD_PER_STEP_TOWARDS_FOOD  # penalty for getting further

        # Stop if we played too long without getting food
        if ((self.stepNum - self.last_food_step) > self.MAX_STEPS_AFTER_FOOD):
            done = True
        self.stepNum += 1

        return self._get_obs(), reward, done, {}

    def render(self):
        print(self.grid)


    def close(self):
        pass

