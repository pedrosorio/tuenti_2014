from collections import deque

T = int(raw_input())
#0 - right, 1 - down
#2 - left, 3 - up
#map from directon to (dy,dx,new_direction)
moves = {0: [[0,1,0], [1,0,1]],
         1: [[1,0,1], [0,-1,2]],
         2: [[0,-1,2], [-1,0,3]],
         3: [[-1,0,3], [0,1,0]]}

ERROR_VALUE = 1000000

#yeah, yeah, I know I should have used bfs
#back in the problem where the engineers were
#swapped around the table and instead I did a
#stupidly complicated A* with a nice heuristic
#that was useless because it took longer than 
#the bfs itself, but this is a simple bfs so
#take that
def bfs(city, start, goal):
  N = len(city)
  M = len(city[0])
  visited = set([start])
  Q = deque([start + (0,)])
  while Q:
    #yeah, yeah we don't check if the start == goal
    #not possible for this problem
    i, j, dr, dst = Q.pop()
    dst += 1
    for mov in moves[dr]:
      ni = mov[0] + i
      nj = mov[1] + j
      newdr = mov[2]
      if ni >= 0 and ni < N and nj >= 0 and nj < M:
        if (ni, nj) == goal:
          return dst
        if city[ni][nj] != "#" and (ni, nj, newdr) not in visited:
          Q.appendleft((ni, nj, newdr, dst))
          visited.add((ni, nj, newdr))
  return ERROR_VALUE #a gazzillion

for test in xrange(1,T+1):
  M, N = map(int, raw_input().split())
  city = [raw_input() for i in xrange(N)]
  for i in xrange(N):
    for j in xrange(M):
      if city[i][j] == 'S':
        start = (i,j)
      elif city[i][j] == 'X':
        goal = (i,j)
  min_dist = min([bfs(city, start + (sdir,), goal) for sdir in xrange(4)]) 
  if min_dist == ERROR_VALUE:
    min_dist = "ERROR"
  print "Case #" + str(test) + ": " + str(min_dist)

