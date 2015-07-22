import numpy as np
import pylab
def mean(seq):  #simplest computation of mean
    """Return mean of values in `seq`."""
    n = len(seq)
    return sum(seq)/float(n)

def transpose(seqseq): #simple 2-dimensional transpose
    """Return transpose of `seqseq`."""
    return zip(*seqseq)

def topscore_playertypes(player):
    """Return list of best (maximum payoff) player types."""
    best_types = [player.playertype]
    best_payoff = player.get_payoff()
    for opponent in player.players_played:
        payoff = opponent.get_payoff()
        if payoff > best_payoff:
            best_payoff = payoff
            best_types = [opponent.playertype]
        elif payoff == best_payoff:
            best_types.append(opponent.playertype)
    return best_types

def maxmin_playertypes(player):
    """Return list of best (maxmin payoff) player types."""
    # initialize mapping (playertypes -> payoffs)
    pt2po = dict()
    # find minimum payoff for each encountered playertype
    pt2po[ player.playertype ] = player.get_payoff()
    for n in player.get_neighbors():
        pt, po = n.playertype, n.get_payoff()
        try:
            if pt2po[pt] > po:
                pt2po[pt] = po
        except KeyError:
            pt2po[pt] = po
    # find best playertype (max of minimum payoffs)
    maxmin = max( pt2po.itervalues() )
    best_playertypes = [ pt for pt in pt2po if pt2po[pt]==maxmin ]
    return best_playertypes



def random_pairs_of(players):
    """Return all of players as random pairs."""
    # copy player list
    players = list( players )
    # shuffle the new player list in place
    random.shuffle(players)
    # yield the shuffled players, 2 at a time
    player_iter = iter(players)
    return izip(player_iter, player_iter)

def compute_neighbors(player, grid):
    """Return neighbors of `player` on `grid`."""
    player_row, player_col = player.gridlocation
    nrows, ncols = grid.nrows, grid.ncols
    players2d = grid.players2d
    # initialize list of neighbors
    neighbors = list()
    # append all neighbors to list
    for offset in grid.neighborhood:
        dc, dr = offset      #note: x,y neighborhood
        r = (player_row + dr) % nrows
        c = (player_col + dc) % ncols
        neighbor = players2d[r][c]
        neighbors.append(neighbor)
    return neighbors

def count_player_types(players):
    """Return map (playertype -> frequency) for `players`."""
    ptype_counts = defaultdict(int) #empty dictionary, default count is 0
    for player in players:
        ptype_counts[ player.playertype ] += 1
    return ptype_counts

class RandomMover:
    def move(self):
        return np.random.uniform(0, 1) < 0.5

## GAME: RanomMover
# create a payoff matrix and two players
PAYOFFMAT = [ [(3,3),(0,5)] , [(5,0),(1,1)] ]
player1 = RandomMover()
player2 = RandomMover()
# get a move from each player
move1 = player1.move()
move2 = player2.move()
# retrieve and print the payoffs
pay1, pay2 = PAYOFFMAT[move1] [move2]
print "Player1 payoff: ", pay1
print "Player2 payoff: ", pay2

class RandomPlayer:
    def __init__(self, p=0.5):
        self.p_defect = p 
    def move(self, game):
        return np.random.uniform(0,1) < self.p_defect
    def record(self, game):
        pass

class SimpleGame:
    def __init__(self, player1, player2, payoffmat):
        #initialize instance attributes
        self.players = [player1, player2]
        self.payoffmat = payoffmat
        self.history = list()
    def run(self, game_iter=4):
        # unpack the two players
        player1, player2 = self.players
        # for each iteration, get new moves and append these to history
        for iteration in range(game_iter):
            newmoves = player1.move(self), player2.move(self)
            self.history.append(newmoves)
        # prompt two players to record the game played (i.e, 'self')
        player1.record(self); player2.record(self)
    def payoff(self):
        # unpack the two players
        player1, player2 = self.players
        # generate a payoff pair for each game iteration
        payoffs = (self.payoffmat[m1][m2] for (m1, m2) in self.history)
        # transpose to get a payof sequence for each player
        pay1, pay2 = transpose(payoffs)
        # return a mapping of each player to its mean payoff
        return { player1:mean(pay1), player2:mean(pay2) }

## GAME: SimpleGame with RanomPlayer
# create a payoff matrix and two players
PAYOFFMAT = [ [(3,3),(0,5)] , [(5,0),(1,1)] ]
player1 = RandomPlayer()
player2 = RandomPlayer()
# create and run game
game = SimpleGame(player1, player2, PAYOFFMAT)
game.run()
# retrieve and print the payoffs
payoffs = game.payoff()
print "Player1 payoff: ", pay1
print "Player2 payoff: ", pay2

class SimplePlayer:
    def __init__(self, playertype):
        self.playertype = playertype
        self.reset()
    def reset(self):
        self.games_played = list() 
        self.players_played = list()
    def move(self, game):
        # delegate move to player type
        return self.playertype.move(self, game)
    def record(self, game):
        self.games_played.append(game)
        opponent = game.opponents[self]
        self.players_played.append(opponent)

class CDIPlayerType:
    def __init__(self, p_cdi=(0.5, 0.5, 0.5)):
        self.p_cdi = p_cdi
    def move(self, player, game):
        # get opponent and learn her last move
        opponent = game.opponents[player]
        last_move = game.get_last_move(opponent)
        # respond to opponent's last move
        if last_move is None:
            p_defect = self.p_cdi[-1]
        else:
            p_defect = self.p_cdi[last_move]
        return np.random.uniform(0, 1) < p_defect

class CDIGame (SimpleGame):
    def __init__(self, player1, player2, payoffmat):
        #begin initialization with `__init__1 from `SimpleGame`
        SimpleGame.__init__(self, player1, player2, payoffmat)
        # initialize new data attribute
        self.opponents = {player1:player2, player2:player1}
    def get_last_move(self, player):
        # if history not empty, return prior move of `player`
        if self.history:
            player_idx = self.players.index(player)
            last_move = self.history[-1] [player_idx]
        else:
            last_move = None
        return last_move

## Game: CDIGame with SimplePlayer
# create a payoff matrix with two players (with playertypes)
PAYOFFMAT = [ [(3,3),(0,5)] , [(5,0),(1,1)] ]
ptype1 = CDIPlayerType()
ptype2 = CDIPlayerType()
player1 = SimplePlayer(ptype1)
player2 = SimplePlayer(ptype2)
# create and run th game
game = CDIGame(player1, player2, PAYOFFMAT)
game.run()
# retrieve and print the payoffs
payoffs = game.payoff()
print "Player1 payoff: ", payoffs[player1]
print "Player2 payoff: ", payoffs[player2]

class SoupPlayer(SimplePlayer):
    def evolve(self):
        self.playertype = self.next_playertype
    def get_payoff(self):
        return sum( game.payoff() [self] for game in self.games_played )
    def choose_next_type(self):
        # find the playertype(s) producing the highest score(s)
        best_playertypes = topscore_playertypes(self)
        # choose randomly from these best playertypes
        self.next_playertype = random.choice(best_playertypes)

class SoupRound:
    def __init__(self, players, payoffmat):
        self.players = players
        self.payoffmat = payoffmat
    def run(self):
        payoff_matrix = self.payoffmat
        for player1, player2 in random_pairs_of(self.players):
            game = CDIGame(player1, player2, payoff_matrix)
            game.run


        
        


