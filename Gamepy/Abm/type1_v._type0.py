import Abm
import matplotlib

# Type 1 v. Type 0
# q = 0.75
# sigma = 2
number_of_agents = 1000
generations = 100
rounds_per_generation = 5
death_rate = .1
mutation_rate = .2
q = 0.75
sigma = 2 
row_matrix = [[1,3], [0+(q*sigma),2+(q*sigma)]]
col_matrix = [[1,0], [3,2]]

g = Abm.ABM(number_of_agents, generations, rounds_per_generation, death_rate, mutation_rate, row_matrix, col_matrix)

g.simulate(plot=True)

# q = 0.5
# sigma = 2

number_of_agents = 1000
generations = 100
rounds_per_generation = 5
death_rate = .1
mutation_rate = .2
q = 0.5
sigma = 2 
row_matrix = [[1,3], [0+(q*sigma),2+(q*sigma)]]
col_matrix = [[1,0], [3,2]]

g = Abm.ABM(number_of_agents, generations, rounds_per_generation, death_rate, mutation_rate, row_matrix, col_matrix)

g.simulate(plot=True)

# q = 0.25
# sigma = 2

number_of_agents = 1000
generations = 100
rounds_per_generation = 5
death_rate = .1
mutation_rate = .2
q = 0.25
sigma = 2 
row_matrix = [[1,3], [0+(q*sigma),2+(q*sigma)]]
col_matrix = [[1,0], [3,2]]

g = Abm.ABM(number_of_agents, generations, rounds_per_generation, death_rate, mutation_rate, row_matrix, col_matrix)

g.simulate(plot=True)