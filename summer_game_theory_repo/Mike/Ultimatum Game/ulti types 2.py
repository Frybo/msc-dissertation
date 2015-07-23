
import random
from operator import itemgetter



# PARAMETERS FOR THE GAME

N = 40 # Population size
R = 20 # Number of games per match
G = 20 # Number of generations
S = 10 # Number of new members introduced/killed in the population after each generation
A = 1 # Amount of adaptation for type 3 players
counter = 0
gen = 0

Average = []

class Player():
        def __init__(self):
                self.give = random.randint(0,100)
                self.ultim = random.randint(0,100)
                self.bank = 0
                self.type = random.randint(1,3)


#Type 1: Stay the course
#Always stick to their guns

#Type 2: TFT
#If they play first, they'll give the normal amount
# if they play second, then in the next instance of the game
# they will offer what their partner offered in the previous round

#Type 3: Adapter
# If they play first and their offer is rejected, they will increase it in the following round
# If they play first and their offer is accepted, they will decrease it in the following round
# If they play second and reject an offer, then they will decrease ultimatum value next round
         
def make_player(i):
        p = Player()
        player = [p.give, p.ultim, p.bank, p.type, i+1]
        return player

Population =[]        
for i in range(N):
        counter = counter + 1
        Population.append(make_player(i))

def game(p1,p2):
    gofirst = random.randint(1,2)
    for i in range(R):
        if (gofirst % 2 == 0):
            gofirst = gofirst + 1
            gift = p1[0]
            ultimatum = p2[1]
            if gift < ultimatum:
                p1[2] = p1[2] + 0
                p2[2] = p2[2] + 0
                if p1[3] == 3:
                    p1[0] += A
                if p2[3] == 3:
                    p2[1] -=A
                if p2[3] == 2:
                    p2[0] = p1[0]
            if gift >= ultimatum:
                p1[2] = p1[2] + 100 - gift
                p2[2] = p2[2] + gift
                if p1[3] ==3:
                    p1[0] -=A
                if p2[3] == 2:
                    p2[0] = p1[0]
            p1[0] = gift
        else:
            gofirst = gofirst + 1
            gift = p2[0]
            ultimatum = p1[1]
            if gift < ultimatum:
                p1[2] = p1[2] + 0
                p2[2] = p2[2] + 0
                if p2[3] == 3:
                    p2[0] += A
                if p1[3] == 3:
                    p1[1] -=A
                if p1[3] == 2:
                    p1[0] = p2[0]
            if gift >= ultimatum:
                p2[2] = p2[2] + 100 - gift
                p1[2] = p1[2] + gift
                if p2[3] ==3:
                    p2[0] -=A
                if p1[3] == 2:
                    p1[0] = p2[0]
            p2[0] = gift
    return p1[2], p2[2]

##def match(p1,p2):
##    numrounds = R
##    i=1
##    while i <= numrounds:
##        game(p1,p2)
##        i=i+1
##    return p1[2], p2[2]

def Generation(popu):
        for k in range(len(popu)):
                p1 = popu[k]
                for i in range(len(popu)):
                        p2= popu[i]
                        game(p1, p2)
        sorted_population = tuple(sorted(popu, key = itemgetter(2)))
        popu = Update(sorted_population)
        return popu

def Update(sortpop):
        global counter
        global gen
        global Average
        #global S
        sumgifts = 0
        sumulti=0
        poppy = list(sortpop)
        for elem in poppy:
                print elem
        print "*******"
        for i in range(N):
                sumgifts = sumgifts + sortpop[i][0]
                sumulti = sumulti + sortpop[i][1]
        Average.append((sumgifts/ N, sumulti/N))
        for i in range(S):
                poppy[i] = make_player(counter + 1 + i)
        for i in range(N):
                poppy[i][2]=0     
        counter = counter + S
        #S = S - 1
        gen = gen + 1
        return poppy

def Simulation(popu):
        for i in range(G):
                popu = Generation(popu)
        return popu


for elem in Simulation(Population):
        print elem

