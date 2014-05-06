from collections import defaultdict
import itertools

#why store a huge 2D array when we can just hash everything?
track = defaultdict(itertools.repeat(" ").next)
line_input = raw_input()
#reorder the track so we know we begin in the finish straight
start_index = line_input.find("#")
line_input = line_input[start_index:] + line_input[:start_index]
x,y = 0,0
dx,dy = 1,0
max_x, max_y, min_x, min_y = 0,0,0,0
#Go through the line, keeping track of the edges of the track
#And hashing the positions the track touches
for c in line_input:
  max_x = max(x, max_x)
  max_y = max(y, max_y)
  min_x = min(x, min_x)
  min_y = min(y, min_y)
  if c == "/":
    dx,dy = -dy,-dx
  elif c == "\\":
    dx,dy = dy,dx
  elif c == "-" and dy != 0:
    c = "|"
  track[(x,y)] = c
  x += dx
  y += dy

for y in xrange(min_y, max_y+1):
  print ''.join([track[(x,y)] for x in xrange(min_x, max_x+1)]) 
