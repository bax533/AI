import random
import math
from queue import Queue


kmoves = [(-1,0), (0,1), (1,0), (0,-1)]
movname= ['U','R', 'D', 'L']

movDict = {
	'U' : (-1,0),
	'R' : (0, 1),
	'D' : (1, 0),
	'L' : (0,-1)
}


endpoints = set()
startpoints_all = []
startpoints_reduced = []
walls = set()


	
def random_heuristic():
	moves = ''
	prev_move = -1


	for i in range(0, 10):
		moves += 'R'
		moves += 'D'

	for i in range(0, 10):
		moves += 'U'
		moves += 'L'

	while(len(moves) <=75):
		move = random.randint(0, 3)
		while(move == prev_move):
			move = random.randint(0,3)

		prev_move = (move + 2)%4

		moves += movname[move]

	for i in range(0, 13):
		moves+= 'L'
		moves+= 'U'
	
	return moves
	
	


def solve():
	q = Queue()
	q.put((frozenset(startpoints_reduced[:]), ''))

	vis = set()

	while(not q.empty()):
		top = q.get()
		positions = top[0]
		moves = top[1]
		

		if(len(moves) < 55):
			allPoints = True
			for p in positions:
				if (p not in endpoints):
					allPoints = False
					break

			if(allPoints):
				return moves
			
			for move in range(0, 4):
				#if(move==prev):
				#	continue
				new_positions = set()
				for pos in positions:
					curPos = pos
					if((curPos[0] + kmoves[move][0], curPos[1]+kmoves[move][1]) not in walls):
						curPos = (curPos[0] + kmoves[move][0], curPos[1]+kmoves[move][1])
					new_positions.add(curPos)
				frozenPos = frozenset(new_positions)
				if(frozenPos not in vis):
					q.put((frozenPos, moves+movname[move]))
					vis.add(frozenPos)
		
	return 'notfound'

def getInput(fileName):

	f = open(fileName, "r")
	board = f.readlines()
	f.close()

	N = len(board)
	M = len(board[0])-1

	for l in range(N):
		for c in range(M):
			if(board[l][c] == '#'):
				walls.add((l, c))
			elif(board[l][c] == 'S'):
				startpoints_all.append((l, c))
			elif(board[l][c] == 'B'):
				startpoints_all.append((l, c))
				endpoints.add((l, c))
			elif(board[l][c] == 'G'):
				endpoints.add((l, c))

def mergeStarts(mvs):
	
	startsCopy = startpoints_all[:]
	tmpStarts = []
	for start in startsCopy:
		pos = start
		for move in mvs:
			if((pos[0]+movDict[move][0], pos[1]+movDict[move][1]) not in walls):
				pos = (pos[0]+movDict[move][0], pos[1]+movDict[move][1])
		if(pos not in tmpStarts):
			tmpStarts.append(pos)
	return tmpStarts



with open('zad_output.txt', 'w') as out:
	getInput('zad_input.txt')
	firstMoves = ''
	best = len(startpoints_all)

	for i in range(0, 60):
		ret = random_heuristic()
		merged = mergeStarts(ret)
		if(len(merged) < best):
			firstMoves = ret
			startpoints_reduced = merged[:]
			best = len(merged)

	print(len(startpoints_reduced))
	res = 'notfound'
	while(res == 'notfound'):
		res = solve()
	out.write(firstMoves + res)
	print('\n', firstMoves + res, '\n')
	startpoints = []
	endpoints = []
	walls = []