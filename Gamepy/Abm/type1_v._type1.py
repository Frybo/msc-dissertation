import Abm
import matplotlib

# Type 1 vs. Type 1
# q = 0.75
# sigma = 0.8
number_of_agents = 1000
generations = 100
rounds_per_generation = 5
death_rate = .1
mutation_rate = .2
q = 0.75
sigma = 2 
row_matrix = [[1,3], [0+(q*sigma),2+(q*sigma)]]
col_matrix = [[1,0+(q*sigma)], [3,2+(q*sigma)]]

g = Abm.ABM(number_of_agents, generations, rounds_per_generation, death_rate, mutation_rate, row_matrix, col_matrix)

g.simulate(plot=True)

# q = 0.5
# sigma = 0.8

number_of_agents = 1000
generations = 100
rounds_per_generation = 5
death_rate = .1
mutation_rate = .2
q = 0.5
sigma = 2
row_matrix = [[1,3], [0+(q*sigma),2+(q*sigma)]]
col_matrix = [[1,0+(q*sigma)], [3,2+(q*sigma)]]

g = Abm.ABM(number_of_agents, generations, rounds_per_generation, death_rate, mutation_rate, row_matrix, col_matrix)

g.simulate(plot=True)

# q = 0.25
# sigma = 0.8

number_of_agents = 1000
generations = 100
rounds_per_generation = 5
death_rate = .1
mutation_rate = .2
q = 0.25
sigma = 2
row_matrix = [[1,3], [0+(q*sigma),2+(q*sigma)]]
col_matrix = [[1,0+(q*sigma)], [3,2+(q*sigma)]]

g = Abm.ABM(number_of_agents, generations, rounds_per_generation, death_rate, mutation_rate, row_matrix, col_matrix)

g.simulate(plot=True)