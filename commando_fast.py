import random
import math
from queue import Queue
from queue import PriorityQueue


kmoves = [(-1,0), (0,1), (1,0), (0,-1)]
movname= ['U','R', 'D', 'L']

movDict = {
	'U' : (-1,0),
	'R' : (0, 1),
	'D' : (1, 0),
	'L' : (0,-1)
}


endpoints = set()
startpoints_all = set()
walls = set()

board = [[]]
N = 0
M = 0

dists = {}


def manhattan(x, y):
	return abs(x[0]-y[0]) + abs(x[1]-y[1])


def distWithWalls(x, end):
	q = Queue()
	vis = set()
	q.put((x, 0))
	vis.add(x)
	while(not q.empty()):
		top = q.get()
		pos = top[0]
		ret = top[1]

		if(pos == end):
			return ret

		for it in range(0, 4):
			newPos=(pos[0] + kmoves[it][0], pos[1] + kmoves[it][1])
			if(newPos not in walls and newPos not in vis):
				vis.add(newPos)
				q.put( (newPos, ret+1) )
 

class State:
	def __init__(self, positions, moves):
		self.positions = positions
		self.fVal = self.f() + len(moves)
		self.moves = moves
		
	def checkPoints(self):
		for pos in self.positions:
			if pos not in endpoints:
				return False
		return True

	def f(self):
		val = 0
		for x in self.positions:
			min_d=dists[x]
			if(min_d>val):
				val = min_d
		return val

	def __hash__(self):
		return hash(self.fVal)^hash(self.positions)

	def __eq__(self, o):
		return self.positions == o.positions

	def __lt__(self, o):
		return self.fVal < o.fVal

	def __le__(self, o):
		return self.fVal <= o.fVal

	def __gt__(self, o):
		return self.fVal > o.fVal

	def __ge__(self, o):
		return self.fVal >= o.fVal
	
	
def Heura(state):
	q = PriorityQueue()
	q.put(state)
	vis = set()
	vis.add(state)
	while(not q.empty()):
		curState = q.get()

		if(curState.checkPoints()):
			return curState.moves

		for m in range(0,4):
			newPositions = set()
			for pos in curState.positions:
				newPos = (pos[0]+kmoves[m][0], pos[1] + kmoves[m][1]) 
				if(newPos not in walls):
					newPositions.add(newPos)
				else:
					newPositions.add(pos)

			newState = State(frozenset(newPositions), curState.moves + movname[m])
			
			if(newState not in vis):
				vis.add(newState)
				q.put(newState)
	return 'notfound'

#RRRRRUURUUUDD 
#RRRRUUUURDRD


def setDists(n, m):
	for l in range(n):
		for c in range(m):
			if((l, c) in walls):
				dists[(l,c)] = 100000
				continue
			mini = 100000
			for e in endpoints:
				distCur = distWithWalls((l, c), e)
				if(distCur < mini):
					mini = distCur
			dists[(l,c)] = mini

def getInput(fileName):

	f = open(fileName, "r")
	board = f.readlines()
	f.close()

	N = len(board)
	M = len(board[0])-1
	e = set()
	w = set()

	for l in range(N):
		for c in range(M):
			if(board[l][c] == '#'):
				walls.add((l, c))
			elif(board[l][c] == 'S'):
				startpoints_all.add((l, c))
			elif(board[l][c] == 'B'):
				startpoints_all.add((l, c))
				endpoints.add((l, c))
			elif(board[l][c] == 'G'):
				endpoints.add((l, c))

	setDists(N, M)



with open('zad_output.txt', 'w') as out:
	getInput('zad_input.txt')
	ret = Heura(State(frozenset(startpoints_all.copy()), ''))

	out.write(ret)
	print('\n', ret, '\n')
