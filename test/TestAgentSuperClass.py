import unittest
from Agent import Agent

a1 = Agent()
a2 = Agent(agent_length=2, agent_height=3, lowest_row=4, least_col=6)
class AgentSuperClassTest(unittest.TestCase):
    def test_default_constructor(self):
        self.assertEquals((1,1), a1.get_agent_size())
        self.assertEquals((0,0), a1.get_position())

    def test_custom_construct_values(self):
        self.assertEquals((4,6), a2.get_position())
        self.assertEquals((2,3), a2.get_agent_size())

    def test_raise_constructor_errors(self):
        with self.assertRaises(ValueError):
            Agent(agent_length= 0)

        with self.assertRaises(ValueError):
            Agent(agent_height= 0)

        with self.assertRaises(ValueError):
            Agent(lowest_row= -1)

        with self.assertRaises(ValueError):
            Agent(least_col= -1)

    def test_get_min_col_boundary(self):
        a1_col_min = a1.get_col_boundaries()[0]
        a2_col_min = a2.get_col_boundaries()[0]

        self.assertEquals(0, a1_col_min)

        # i.e. if lowest col is 4 and length is 2
        # agent occupies spaces 4, and 5, not 6
        self.assertEquals(6, a2_col_min)

    def test_get_max_col_boundary(self):
        a1_max_col_b = a1.get_max_col_boundary()
        a2_max_col_b = a2.get_max_col_boundary()
        self.assertEquals(0, a1_max_col_b)
        self.assertEquals(7, a2_max_col_b)

    def test_get_col_boundaries(self):
        self.assertEquals((0,0), a1.get_col_boundaries())
        self.assertEquals((6,7), a2.get_col_boundaries())

    def test_get_min_row_boundary(self):
        a1_min_row_b = a1.lowest_row
        a2_min_row_b = a2.lowest_row

        self.assertEquals(0,a1_min_row_b)
        self.assertEquals(4, a2_min_row_b)

    def test_get_row_boundaries(self):
        a1_row_bounds = a1.get_row_boundaries()
        a2_row_bounds = a2.get_row_boundaries()

        self.assertEquals((0,0), a1_row_bounds)
        self.assertEquals((4,6), a2_row_bounds)





def main():
    unittest.main(verbosity=3)

if __name__ == '__main__':
    main()