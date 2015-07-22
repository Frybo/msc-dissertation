import matplotlib.pyplot as plt 
import itertools
import random
import copy
from __future__ import division 

class Agent():
	#Agent Class
	def __init__(self, strategy):
		self.strategy = strategy
		self.utility = 0

def kill_one_agent_with_given_utility(agents, utility):
	#Used to delete an agent
	number_of_agents = len(agents)
	k = 0
	while len(agents) == number_of_agents:
		if agents[k].utility == utility:
			del agents[k]
		k += 1

def reproduce_one_agent_with_given_utility(agents, utility, socialization_rate, strategies):
	#Deep copy an agent with a given utility. When copying an agent there is a potential socialization that will make the new agent have a different strategy.
    number_of_agents = len(agents)
    k = 0
    while len(agents) == number_of_agents:
    	if agents[k].utility == utility:
    		agents.append(copy.deepcopy(agents[k]))
    		if random.random() < socialization_rate:
    			agents[-1].strategy = random.choice([s for s in strategies if s != agents[-1].strategy])
    	k += 1

def return_current_strategy_distribution(agents, strategies):
	#This will return the current strategy distribution amongst a set of agents.
	frequencies = []
	for s in strategies:
		frequencies.append(0)
		for e in agents:
			if e.strategy == s:
				frequencies[-1] += 1
	return [e / len(agents) for e in frequencies]


class Model():
	#define the bowles model
	def __init__(self, number_of_agents, generations, rounds_per_generation, death_rate, number_of_deaths_per_generation, )