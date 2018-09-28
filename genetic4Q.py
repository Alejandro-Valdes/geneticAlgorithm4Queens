import random
import numpy as np
from pandas import DataFrame 

numbers = ['00','10','01','11']
binRep = 2

def getPositions(config):
	positions = []
	for i in range(0, 4):
		positions.append(int((config[i*2:i*2+2]),2))
	return positions

def getBoard(config):
	board = np.chararray((4,4))
	board[:] = '*'
	positions = getPositions(config)
	for i, pos in enumerate(positions):
		board[pos][i] = 'Q'
	return board

def getDiagonals(a):
	diags = [a[::-1,:].diagonal(i) for i in range(-a.shape[0]+1,a.shape[1])]
	diags.extend(a.diagonal(i) for i in range(a.shape[1]-1,-a.shape[0],-1))
	return np.array([n for n in diags])

def getClashes(ls):
	clashes = 0
	for x in ls:
		x = x.decode()
		if len(x) > 1:
			clashes_x = sum(x == 'Q')
			if clashes_x > 1:
				clashes += clashes_x * (clashes_x - 1)
	return clashes

def getAptitudes(pop):
	aptSum = 0
	acum = 0
	for p in pop:
		aptSum+=p[2]

	for p in pop:
		prob = p[2] / aptSum
		acum += prob
		p.append(prob)
		p.append(acum)
	return pop

def getFitness(individual):
	positions = individual[0]
	board = individual[1]
	diagonals = getDiagonals(board)
	horizontal_clash = getClashes(board)
	vertical_clash = getClashes(diagonals)
	fitness = 6 - (horizontal_clash + vertical_clash) // 2


	return fitness

def getInitialPopulation(k=4):
	population = []
	for i in range(k):
		offsrpring = ''
		for j in range(0,len(numbers)):
			offsrpring += random.choice(numbers)
		p = [offsrpring, getBoard(offsrpring)]
		p.append(getFitness(p))
		population.append(p)
	population = getAptitudes(population)
	return population

def getMutation(individual):
	n = 2
	cromosome = [individual[i:i+n] for i in range(0, len(individual), n)]
	mutation = ''
	for n in cromosome:
		if random.random() < 0.2:
			n = random.choice(numbers)
		mutation += n
	return mutation

def reproduce(population):
	parents = []
	new_pop = []
	for i in range(4):
		rand = random.random()
		for p in population:
			if p[4] >= rand:
				parents.append(p[0])
				break
	seed = random.randint(0,8) + 1

	child = getMutation(parents[0][:seed] + parents[1][seed:])
	new_pop.append([child])
	child = getMutation(parents[0][seed:] + parents[1][:seed])
	new_pop.append([child])

	seed = random.randint(0,8) + 1
	child = getMutation(parents[2][:seed] + parents[3][seed:])
	new_pop.append([child])
	child = getMutation(parents[2][seed:] + parents[3][:seed])
	new_pop.append([child])

	for p in new_pop:
		p.append(getBoard(p[0]))
		p.append(getFitness(p))

	new_pop = getAptitudes(new_pop)

	return new_pop


def printBoard(individual):
	print('Board - ' + individual[0])
	print('Fitness - ' + str(individual[2]))
	print('Cross Prob - ' + str(individual[3]))
	print('Acum Prob - ' + str(individual[4]))

	print(DataFrame(individual[1].decode()))
	print('*' * 40)

pop = getInitialPopulation()

won = False
while not won:
	for p in pop:
		if p[2] == 6:
			print('WON')
			printBoard(p)
			won = True
			break
		printBoard(p)

	pop = reproduce(pop)


