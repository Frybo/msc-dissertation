import random
import math
import sys

#Simulation of the Prisoner Dilemma.
#Iterated through a genetic algorithm.
#The algorithm punishes agents for
#accumulating prison years.

class adaptableClass:
	"""The class of the agents in the simulation. 
	Each agent is an instance of this class."""

	generation = 0
	fitness = 0.5
	dna = []
	tellchance = 0.0
	prisonyears = 0

	def __init__(self, generation, dna):
		self.generation = generation
		self.dna = dna

	def translateDNA(self):
		"""Translates the DNA into the chance of giving up the other party."""

		for g in self.dna:

#			If you have changed the length of the DNA, make sure to change the tellchance here.
#			You may change the tellchance without changing the length. The system ensures. that
#			tellchance can't go beyond 100%.

			if g == 0:
				self.tellchance -= 0.25
			else:
				self.tellchance += 0.25
		if self.tellchance > 1:
			self.tellchance = 1
		elif self.tellchance < 0:
			self.tellchance = 0

def generationGenerator(popsize):
	"""Generates the initial generation (Generation 0)."""

	population = []


	for person in range(popsize):
		currentdna = []

#		Fills the list currentdna with a new, randomly generated set of genes.
#		The range can be changed for longer or shorter DNA.
#		If you are changing the argument of range, be sure to change the translation method
#		in adaptable class. 
		
		for gene in range(4):		
			randnum = random.randint(0, 1)
			currentdna.append(randnum)
	
		person = adaptableClass(0, currentdna)
		population.append(person)

	return population

def fitnessCalculator(population):
	"""Calculates the weight of the agent in the gene pool.
	Plays out the agent interactions."""
	
	endpoint = len(population)
	
	for spec in population:
		spec.translateDNA() 

#	Plays out the interactions.

	for p in range(len(population)):
		startingpoint = p + 1
		for member in range(startingpoint, endpoint):
			tell1 = population[p].tellchance - (float(random.randrange(0, 100, 1)) / 100)
			tell2 = population[member].tellchance - (float(random.randrange(0, 100, 1)) / 100)

			if tell1 > 0 and tell2 > 0:
				population[p].prisonyears += 1
				population[member].prisonyears += 1
			elif tell1 > 0 and tell2 <= 0:
				population[member].prisonyears += 5
			elif tell1 <= 0 and tell2 > 0:
				population[p].prisonyears += 5

#		Calculate the fitness value of the agent. If the years spent in prison is 0
#		set the fitness to 1000 (which in relation to the other expected values is 
#		quite high).

		if population[p].prisonyears != 0:		
			population[p].fitness = math.floor((1.0/population[p].prisonyears)*1000)

		else:
			population[p].fitness = 1000

def nextgen(prevgen, popsize):
	"""Creates the gene pool and simulates the interactions. 
	The resulting genes are assigned to new agents (instances of
	adaptableClass)"""

	pool = []
	population = []
	generation = prevgen[1].generation + 1

	for q in prevgen:
		for n in range(int(q.fitness)):
			pool.append(q.dna)

#	Takes a random sample of 2 parent DNAs and generates a child DNA.
	
	for m in range(popsize):
		parents = random.sample(pool, 2)
		newgene = []
		for i in range(len(parents[1])):
			source = random.choice(parents)
			newgene.append(source[i])
		
		newspecimen = adaptableClass(generation, newgene)
		population.append(newspecimen)

	return population

def main():

	generations = int(sys.argv[1])
	populationnumber = int(sys.argv[2])
	
	generationlist = []
#	Generates the initial population.
	generationlist.append(generationGenerator(populationnumber))
	fitnessCalculator(generationlist[0])

#	Generates all other generations.	

	for iteration in range(1, generations):
		nextg = nextgen(generationlist[iteration - 1], populationnumber)
		generationlist.append(nextg)
		fitnessCalculator(nextg)

#	Creates the human interpretable statistics.

	for stuff in generationlist:
		countdict = {}
		for more in stuff:
			if more.tellchance in countdict:
				countdict[more.tellchance] += 1
			else:
				countdict[more.tellchance] = 1
		sorteddict = sorted(countdict)
		print "\nFrequencies in generation", stuff[1].generation, ":\n"
		print "Prob.   Freq."
		for key in sorteddict:
			freq_percent = (countdict[key]/float(populationnumber))*100		
			print key, "	", freq_percent, "%", int(math.floor(freq_percent)) * "*"

if __name__ == '__main__':
	main()


