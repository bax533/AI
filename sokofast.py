from queue import Queue
from queue import PriorityQueue
import math
import copy

kmoves = [(-1,0), (0,1), (1,0), (0,-1)]
movname= ['U','R', 'D', 'L']

endpoints = set()
endpoints_count = 0
walls = set()
empty = set()

def manhattan(x, y):
	return abs(x[0]-y[0]) + abs(x[1]-y[1])

def dist(x, y):
	return math.sqrt((x[0]-y[0])*(x[0]-y[0]) + (x[1]-y[1])*(x[1]-y[1]))

class Board:
	def __init__(self, keeper, boxes):
		self.keeper = keeper
		self.boxes = boxes
		self.fVal = self.f()
		#self.alreadyOnEnd = alreadyOnEnd

	def boxInCorner(self):
		for box in self.boxes:
			for i in range(0, 4):
				if((box[0]+kmoves[i][0], box[1]+kmoves[i][1]) in walls and (box[0]+kmoves[(i+1)%4][0], box[1]+kmoves[(i+1)%4][1]) in walls):
					return True
		return False

	def f(self):
		ret = 0
		for b in self.boxes:
			minend = 10000
			for e in endpoints:
				if(manhattan(b, e)<minend):
					minend = manhattan(b, e)
			ret += minend
		return ret

	def allBoxes(self):
		for box in self.boxes:
			if(box not in endpoints):
				return False
		return True

	def __hash__(self):
		return  hash(self.keeper) ^ hash(self.fVal) ^ hash(frozenset(self.boxes))

	def __eq__(self, o):
		return self.keeper == o.keeper and self.boxes ==o.boxes and self.fVal == o.fVal

	def __lt__(self, o):
		return self.fVal < o.fVal

	def __le__(self, o):
		return self.fVal <= o.fVal

	def __gt__(self, o):
		return self.fVal > o.fVal

	def __ge__(self, o):
		return self.fVal >= o.fVal
		

def findRoute(board, pos):
	q = PriorityQueue()
	q.put((manhattan(board.keeper, pos), board.keeper,''))
	vis = set()
	vis.add(board.keeper)
	while(not q.empty()):
		top = q.get()
		curPos = top[1]
		moves = top[2]

		if(curPos == pos):
			return moves

		for it in range(len(kmoves)):
			newPos = (curPos[0] + kmoves[it][0], curPos[1] + kmoves[it][1])
			if(newPos not in walls and newPos not in board.boxes and newPos not in vis):
				q.put((manhattan(newPos, pos), newPos, moves + movname[it]))
				vis.add(newPos)
	return 'toolong'


def BFS(brd):
	q = PriorityQueue()
	q.put((brd, ''))
	vis = set()
	vis.add(brd)
	while(not q.empty()):
		top = q.get()
		curBoard = top[0]
		moves = top[1]
		
		#print(curBoard.keeper)
		if('toolong' in moves):
			#print(curBoard.boxes)
			continue

		if(curBoard.allBoxes()):
			return moves

		for box in curBoard.boxes:
			for it in range(len(kmoves)):
				newBox = (box[0] + kmoves[it][0], box[1] + kmoves[it][1])
				pushFrom = (box[0] + kmoves[(it+2)%4][0], box[1] + kmoves[(it+2)%4][1])
				if(newBox not in walls and pushFrom not in walls and newBox not in curBoard.boxes and pushFrom not in curBoard.boxes):
					newBoxes = copy.deepcopy(curBoard.boxes)
					newBoxes.remove(box)
					newBoxes.add(newBox)
					newBoard = Board(box, newBoxes)
					if(newBoard not in vis):
						q.put((newBoard, moves + findRoute(curBoard, pushFrom) + movname[it]))
						vis.add(newBoard)
						


	return 'DULD'


def getInput(fileName):

	board = []
	keeper = (0,0)
	boxes = set()
	plus = False

	stars = 0

	f = open(fileName, "r")
	board = f.readlines()
	f.close()

	N = len(board)
	M = len(board[0])-1

	for l in range(N):
		for c in range(M):
			if(board[l][c] == 'W'):
				walls.add((l, c))
			elif(board[l][c] == 'K'):
				keeper = (l,c)
			elif(board[l][c] == 'B'):
				boxes.add((l, c))
			elif(board[l][c] == 'G'):
				endpoints.add((l,c))
			elif(board[l][c] == '*'):
				stars += 1
				endpoints.add((l,c))
				boxes.add((l,c))
			elif(board[l][c] == '+'):
				keeper = (l, c)
				plus = True
	return Board(keeper, boxes)

with open('zad_output.txt', 'w') as out:
	b = getInput('zad_input.txt')
	res = BFS(b)
	print(res)
	out.write(res + '\n')


