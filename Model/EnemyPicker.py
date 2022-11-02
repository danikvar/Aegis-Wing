import random

from Model.Agents.AgentInterface import AgentInterface

#TODO write tests
class EnemyPicker():

    def __init__(self):
        """
        Constructor for the EnemySpawnBehaviorSuperClass
        """
        #form associative array
        self.enemy_spawn_list = []
        self.enemy_weights = []
        self.initialized = False

    def add_enemy_to_spawn_list(self, enemy: AgentInterface, weight: int):
        """
        Adds an enemy to the spawn list with a weight. The higher
        the weight, the more likely the enemy will be chosen by choose enemy method.
        Throw an error if enemy passed is a player agent
        :param enemy: {AgentInterface}
        :param weight: {int} influences probability of being chosen, cannot be negative or 0
        :return:
        """
        if enemy.isPlayer() == True:
            raise ValueError("Cannot add player to enemy list")

        if weight <= 0:
            raise ValueError("An enemy agent cannot have a weight <= 0 ")

        self.enemy_spawn_list.append(enemy)
        self.enemy_weights.append(weight)

    def initialize_spawn_behavior(self):
        """
        Performs proper checks to make sure choose enemy will not
        cause an error.
        :return: None
        """
        # check probabilities len matches spawn list len because they are
        #supposed to be associative array
        if len(self.enemy_spawn_list) != len(self.enemy_weights):
            raise RuntimeError("ERROR: enemy spawn list and probability mismatch\nPlease check len of spawn list and len weights are the same")

        self.initialized = True

    def choose_enemy(self):
        """
        Chooses an enemy from list of enemies.
        The higher the weight of an enemy, the more likely
        they will be chosen.
        :return: {AgentInterface} enemy chosen
        """
        if self.initialized == False:
            raise RuntimeError("Spawn Behavior not initialized, please call .initialize_spawn_behavior method")
        random.choices(population=self.enemy_spawn_list,
                       weights=self.enemy_weights,
                       k=1)
