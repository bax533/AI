from queue import Queue
import math

Dw = []
Dk = []
DwIdx = []


n = 0
m = 0


def testMakeD():
	n = 11
	opis = [2, 2, 2]
	mozliwe = []

def makeD(opis, curComb, free, placed, curSpace):
	
	if(placed == len(opis)):
		yield curComb + free * '.'
		return

	for spaceLength in range(curSpace, free):
		arr = ''
		arr += spaceLength * '.'
		arr += opis[placed] * '#'
		if(free - spaceLength - opis[placed] >= 0):
			yield from makeD(opis, curComb + arr, free - spaceLength - opis[placed], placed+1, 1)
		elif(len(curComb + arr + free * '.') == n and placed == len(opis) - 1):
			yield curComb + arr + free * '.'

def getInput(fileName):

	global n
	global m

	with open(fileName) as file:
		n, m = [int(x) for x in next(file).split()]
		wierszeOpis = []
		for it in range(n):
			wierszeOpis.append([int(x) for x in next(file).split()])
		
		kolumnyOpis = []
		for it in range(m):
			kolumnyOpis.append([int(x) for x in next(file).split()])

		for wiersz in wierszeOpis:
			temp = []
			for possible in makeD(wiersz, '', m, 0, 0):
				temp.append(possible)
			Dw.append(temp)

		for kolumna in kolumnyOpis:
			temp = []
			for possible in makeD(kolumna, '', n, 0, 0):
				temp.append(possible)
			Dk.append(temp)

def AC3():
	global n
	global m

	q = Queue()
	for i in range(n):
		for j in range(m):
			q.put(((i, 'w'), (j, 'c')))
			q.put(((j, 'c'), (i, 'w')))

	while(not q.empty()):
		X1, X2 = q.get()
		if(Revise(X1, X2)):
			if(X1[1] == 'w' and len(Dw[X1[0]]) == 0):
				return False
			if(X1[1] == 'c' and len(Dk[X1[0]]) == 0):
				return False

			if(X1[1] == 'w'):
				for i in range(m):
					#if(i == X2[0]):
					#	continue
					q.put( ( (i, 'c'), X1) )
			else:
				for i in range(n):
					#if(i == X2[0]):
					#	continue
					q.put( ( (i, 'w'), X1) )
	return True

def Revise(X1, X2):
	revised = False
	if(X1[1] == 'w'):
		for x in Dw[X1[0]]:
			isValue = False
			for y in Dk[X2[0]]:
				if(x[X2[0]] == y[X1[0]]):
					isValue = True
			if(not isValue):
				Dw[X1[0]].remove(x)
				revised = True

		for x in Dk[X2[0]]:
			isValue = False
			for y in Dw[X1[0]]:
				if(x[X1[0]] == y[X2[0]]):
					isValue = True
			if(not isValue):
				Dk[X2[0]].remove(x)
				revised = True
	else:
		for x in Dk[X1[0]]:
			isValue = False
			for y in Dw[X2[0]]:
				if(x[X2[0]] == y[X1[0]]):
					isValue = True
			if(not isValue):
				Dk[X1[0]].remove(x)
				revised = True

		for x in Dw[X2[0]]:
			isValue = False
			for y in Dk[X1[0]]:
				if(x[X1[0]] == y[X2[0]]):
					isValue = True
			if(not isValue):
				Dw[X2[0]].remove(x)
				revised = True
	return revised

def CheckAssignment(assignment, rowsTaken):
	for nr in range(len(assignment[0])):
		exists = 0
		newCol = []
		for colLength in range(len(assignment)):
			if(colLength in rowsTaken):
				newCol.append(assignment[colLength][nr])
			else:
				newCol.append('x')

		for col in Dk[nr]:

			colTake = []
			for it in range(len(col)):
				if(it in rowsTaken):
					colTake.append(col[it])
				else:
					colTake.append('x')

			curColGood = True
			for nr in rowsTaken:
				if(colTake[nr] != newCol[nr]):
					curColGood = False
					break

			if(curColGood):
				exists += 1

		if(exists == 0):
			return False
	return True


def Backtrack(assignment, w, rowsTaken):
	global n
	if(w == n):
		return assignment
	for x in Dw[DwInd[w]]:
		newAssignment = assignment[:]
		newAssignment[DwInd[w]] = x
		if(CheckAssignment(newAssignment, rowsTaken + [DwInd[w]])):
			result = Backtrack(newAssignment, w+1, rowsTaken + [DwInd[w]])
			if('fail' not in result):
				return result
	return assignment + ['fail']

def CheckAssignment1(assignment):
	for nr in range(len(assignment[0])):
		exists = False
		newCol = ''
		for colLength in range(len(assignment)):
			newCol += assignment[colLength][nr]
		for x in Dk[nr]:
			if(x[:len(assignment)] == newCol):
				exists = True
				break
		if(not exists):
			return False
	return True


def Backtrack1(assignment, w):
	global n
	if(w == n):
		return assignment
	for x in Dw[w]:
		newAssignment = assignment + [x]
		if(CheckAssignment1(newAssignment)):
			result = Backtrack1(newAssignment, w+1)
			if('fail' not in result):
				return result
	return assignment + ['fail']

def sortDwBySize():
	for x in range(len(Dw)):
		DwIdx.append(x)
    
	DwCopy = Dw[:]

	for i in range(len(DwCopy)):
		for j in range(len(DwCopy)-1):
			if (len(DwCopy[j])>len(DwCopy[j+1])):
				t = DwIdx[j]
				DwIdx[j] = DwIdx[j+1]
				DwIdx[j+1] = t

				t = DwCopy[j]
				DwCopy[j] = DwCopy[j+1]
				DwCopy[j+1] = t

#test_input()

with open('zad_output.txt', 'w') as out:
	getInput("zad_input.txt")
	res = AC3()
	
	#sortDwBySize()
	#for x in Dw:
	#	print(len(Dw[x]))
		#out.write(x[0] + '\n')


	if(res):
		#pic = Backtrack([('' for x in range(len(Dw)))], 0, [])
		for x in Dw:
			print(x[0])
			out.write(x[0] + '\n')

