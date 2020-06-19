from queue import Queue
from queue import PriorityQueue
import math

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
	def __init__(self, keeper, boxes, alreadyOnEnd):
		self.keeper = keeper
		self.boxes = boxes
		self.fVal = self.f()
		self.alreadyOnEnd = alreadyOnEnd

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
		return  hash(self.keeper) ^ hash(self.fVal) ^ hash(self.alreadyOnEnd)

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
		


def BFS(brd):
	q = Queue()
	q.put((brd,''))
	vis = set()
	vis.add(brd)

	while(not q.empty()):
		top = q.get()
		curBoard = top[0]
		moves = top[1]

		#print(curBoard.keeper)
		if(curBoard.alreadyOnEnd == len(endpoints)):
			return moves

		for it in range(len(kmoves)):
			newkeep = (curBoard.keeper[0] + kmoves[it][0], curBoard.keeper[1] + kmoves[it][1])
			#print(newkeep)
			#if(newkeep[0] < N and newkeep[1] < M):
			if(newkeep not in walls and newkeep not in curBoard.boxes):

				newBoard = Board(newkeep, curBoard.boxes, curBoard.alreadyOnEnd)
				if((newBoard not in vis)):
					vis.add(newBoard)
					q.put((newBoard, moves + movname[it]))

			elif(newkeep in curBoard.boxes):
				
				curOnEnd = curBoard.alreadyOnEnd
				if(newkeep in endpoints):
					curOnEnd -= 1

				newbox = (newkeep[0] + kmoves[it][0], newkeep[1]+ kmoves[it][1])

				newboxes = curBoard.boxes.copy()
				newboxes.remove(newkeep)

				if(newbox in endpoints):
					curOnEnd += 1

				if(newbox not in walls and newbox not in curBoard.boxes):
					newboxes.add(newbox)
					newBoard = Board(newkeep, newboxes, curOnEnd)
					if((newBoard not in vis)):
						vis.add(newBoard)
						q.put((newBoard, moves + movname[it]))

	return 'notFound'

def Astar(brd):
	q = PriorityQueue()
	q.put((brd,''))
	vis = set()
	vis.add(brd)
	while(not q.empty()):
		top = q.get()
		curBoard = top[0]
		moves = top[1]
		#if (curBoard.boxInCorner()):
		#	continue

		if(curBoard.alreadyOnEnd == len(endpoints)):
			return moves

		for it in range(len(kmoves)):
			newkeep = (curBoard.keeper[0] + kmoves[it][0], curBoard.keeper[1] + kmoves[it][1])
			#print(newkeep)
			#if(newkeep[0] < N and newkeep[1] < M):
			if(newkeep not in walls and newkeep not in curBoard.boxes):

				newBoard = Board(newkeep, curBoard.boxes, curBoard.alreadyOnEnd)
				newBoard.fVal += len(moves)+1
				if((newBoard not in vis)):
					vis.add(newBoard)
					q.put((newBoard, moves + movname[it]))

			elif(newkeep in curBoard.boxes):
				
				curOnEnd = curBoard.alreadyOnEnd
				if(newkeep in endpoints):
					curOnEnd -= 1

				newbox = (newkeep[0] + kmoves[it][0], newkeep[1]+ kmoves[it][1])

				newboxes = curBoard.boxes.copy()
				newboxes.remove(newkeep)

				if(newbox in endpoints):
					curOnEnd += 1

				if(newbox not in walls and newbox not in curBoard.boxes):
					newboxes.add(newbox)
					newBoard = Board(newkeep, newboxes, curOnEnd)
					newBoard.fVal += len(moves)+1
					if((newBoard not in vis)):
						vis.add(newBoard)
						q.put((newBoard, moves + movname[it]))

	return 'notFound'
		



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
	return Board(keeper, boxes, stars)

with open('zad_output.txt', 'w') as out:
	b = getInput('zad_input.txt')
	res = BFS(b)
	print(res + '\n')
	out.write(res + '\n')


