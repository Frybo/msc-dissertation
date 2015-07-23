# MAKE SURE TO UPDATE TEST CASE PARAMS IF ADDING NEW PARAMETERS

W = 0.95    # Probability that the game goes on another turn
NUMBER_OF_AGENTS = 64
GENERATIONS = 25
ROUNDS = 64 # Matchups per generation
ENDOWMENT = (1, 0)    # How much each player receives at the start of the game
A = 10    # Multiplier for Investor balance after Investor -> Trustee gift
B = 30    # Multiplier for Investor -> Trustee
C = 1    # Multiplier for Trustee -> Investor
SWAP = False    # Whether or not agents switch roles after each turn
RESET = False    # Whether or not the balance is stored or can still be used
LOG = True    # Whether or not to write to log files
SIM_NAME = "testing" # Name of log subdirectory
MEMORY = 4    # How far back the agents remember
# determine the mix of the new pop when mutating 
# (# breed, # live but not breed, # newcommers)
MUTATION_PARAMS= (20,24,0)    

# For all or nothing, set A your desired investor endowment, 
# B = (A * the multiplier on that endowment), and ENDOWMENT = (1, 0) 