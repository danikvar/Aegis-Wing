import unittest
from Agent import Agent

a1 = Agent()
a2 = Agent(2,3,4,6)
class AgentSuperClassTest(unittest.TestCase):
    def test_default_constructor(self):
        self.assertEquals((1,1), a1.get_agent_size())
        self.assertEquals((0,0), a1.get_position())

    def test_custom_construct_values(self):
        self.assertEquals((4,6), a2.get_position())
        self.assertEquals((2,3), a2.get_agent_size())

    def test_raise_constructor_errors(self):
        with self.assertRaises(ValueError):
            Agent(agent_len_x= 0)

        with self.assertRaises(ValueError):
            Agent(agent_len_y= 0)

        with self.assertRaises(ValueError):
            Agent(pos_x= -1)

        with self.assertRaises(ValueError):
            Agent(pos_y= -1)

    def test_get_min_x_boundary(self):
        a1_x_min = a1.get_x_boundaries()[0]
        a2_x_min = a2.get_x_boundaries()[0]

        self.assertEquals(0, a1_x_min)

        # i.e. if furthest x pos is 4, and x_len is 2
        # agent occupies spaces 3 and 4, not 2, 3, and 4
        self.assertEquals(4, a2_x_min)

    def test_get_x_boundaries(self):
        self.assertEquals((0,0), a1.get_x_boundaries())
        self.assertEquals((3,4), a2.get_x_boundaries())

    def test_get_min_y_boundary(self):
        a1_y_max = a1.get_y_boundaries()[1]
        a2_y_max = a1.get_y_boundaries()[1]

        self.assertEquals(1,a1_y_max)
        self.assertEquals(8, a2_y_max)

    def test_get_y_boundaries(self):
        self.assertEquals((0, 0), a1.get_y_boundaries())
        self.assertEquals((6,8),a2.get_y_boundaries())





def main():
    unittest.main(verbosity=3)

if __name__ == '__main__':
    main()