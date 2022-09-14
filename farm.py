from random import choice
from sys import stdin

FARM_LENGTH = 400
FARM_WIDTH = 600
AREA = FARM_LENGTH * FARM_WIDTH

def neighbors(x,y):
	#Input: x,y are coordinates or the farm grid
	#Output: all the valid neighboring cells on the grid (not filtered based on whether they were visited yet)
	l = [(x-1,y),(x+1,y),(x,y-1),(x,y+1),(x-1,y-1),(x-1,y+1),(x+1,y-1),(x+1,y+1)]
	l = list(filter(lambda x: x[0]>=0 and x[1]>=0 and x[0]<FARM_LENGTH and x[1]<FARM_WIDTH, l))
	return l

def farm(input):
	#Input: the input string of the rectangles
	#Ouput: a sorted list of the fertile areas
	area = {} # to contain areas of the different fertile sectors
	grpId = 0
	notVisited={(i,j) for i in range(FARM_LENGTH) for j in range(FARM_WIDTH)}
	#parse the squares, mark everything inside as visited to avoid later
	for sq in input:
		coordinates = sq.split(' ')
		coordinates = list(map(lambda x: int(x), coordinates))
		for i in range(coordinates[0], coordinates[2]+1):
			for j in range(coordinates[1], coordinates[3]+1):
				if (i,j) in notVisited:
					notVisited.remove((i,j))
	fringe = []
	while len(notVisited) > 0:
		# as long as there are fertile squares left
		if len(fringe) == 0:
			# done with previous sector, start calculating a new one
			# start with a random square that has not been looked at yet
			fringe.append(choice(tuple(notVisited))) #https://stackoverflow.com/questions/15837729/random-choice-from-set-python
			grpId += 1 # new sector
			area[grpId] = 0
		while len(fringe) > 0:
			x,y = fringe.pop()
			if (x,y) in notVisited:
				notVisited.remove((x,y))
				area[grpId] += 1
				n = neighbors(x,y)
				#print(n)
				n = list(filter(lambda x: x in notVisited, n))
				fringe.extend(n) # add non visited neighboring squares on the grid to be added to the sector later
	resp = list(area.values())
	resp.sort()
	return resp

#Testing

assert(farm(['0 292 399 307']) == [116800, 116800])
assert(farm(['48 192 351 207', '48 392 351 407', '120 52 135 547', '260 52 275 547']) == [22816, 192608])
assert(farm(['1 101 100 200', '51 131 70 198']) == [230000]) # square fully inside square
assert(farm(['1 101 100 200', '51 131 70 198', '51 111 115 205']) == [228325]) # square extends 15 out in x, 5 out in y, 5*50+15*90+15*5=1675 less

print("Insert following format: x0 y0 x1 y1,x0 y0 x1 y1,x0 y0 x1 y1,... etc], or ctrl+c to quit")
print("example input: 1 101 100 200,51 131 70 198,51 111 115 205")
for line in stdin:
	try:
		print(farm(line.split(',')))
	except:
		print('probably bad input')
