import Abm
import matplotlib

number_of_agents = 1000
generations = 100
rounds_per_generation = 1
death_rate = .1
mutation_rate = .2
row_matrix = [[100, 15], [500, 500]]
col_matrix = [[0, 0], [3, 5]]

g = Abm.ABM(number_of_agents, generations, rounds_per_generation, death_rate, mutation_rate, row_matrix, col_matrix)

g.simulate(plot=True)