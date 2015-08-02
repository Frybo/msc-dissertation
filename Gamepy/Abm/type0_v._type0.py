import Abm
import matplotlib

# Type 0 vs. Type 0
number_of_agents = 1000
generations = 100
rounds_per_generation = 5
death_rate = .1
mutation_rate = .2
row_matrix = [[1,3], [0,2]]
col_matrix = [[1,0], [3,2]]

g = Abm.ABM(number_of_agents, generations, rounds_per_generation, death_rate, mutation_rate, row_matrix, col_matrix)

g.simulate(plot=True)