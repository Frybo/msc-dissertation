import Abm
import matplotlib
number_of_agents = 1000
generations = 1000
rounds_per_generation = 1
death_rate = .1
mutation_rate = .2
row_matrix = [[0, 0], [-1, 1]]
col_matrix = [[1, -1], [-10, -10]]

g = Abm.ABM(number_of_agents, generations, rounds_per_generation, death_rate, mutation_rate, row_matrix, col_matrix)

g.simulate(plot=True)
