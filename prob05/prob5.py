def get_next_grid(grid):
  grid_h = len(grid)
  grid_w = len(grid[0])
  res_grid = [[0 for j in xrange(grid_w)] for i in xrange(grid_h)]
  for i in xrange(grid_h):
    for j in xrange(grid_w):
      living_nearby = sum(map(sum, [[grid[di][dj] for dj in xrange(max(0,j-1),min(grid_w,j+2))] for di in xrange(max(0,i-1),min(grid_h,i+2))]))
      if grid[i][j] == 0 and living_nearby == 3:
        res_grid[i][j] = 1
      elif grid[i][j] == 1 and (living_nearby == 3 or living_nearby == 4):
        res_grid[i][j] = 1
  return res_grid

def get_hash_grid(grid):
  mult = 0
  hash_code = 0
  grid_h = len(grid)
  grid_w = len(grid[0])
  for i in xrange(grid_h):
    for j in xrange(grid_w):
      if mult == 0:
        mult = 1
      else:
        mult *= 2
      hash_code += mult * grid[i][j]
  return hash_code 

#We know the grids are 8x8 and the hash fits oh so nicely in
#64-bit int, but it doesn't take much effort to generalize
#to a grid of any size
grid_h = 8
grid_w = 8
grid = [[0 for j in xrange(grid_w)] for i in xrange(grid_h)]

for i in xrange(grid_h):
  line = raw_input().strip()
  for j in xrange(grid_w):
    if line[j] == "X":
      grid[i][j] = 1

grid_hashes = {}
step = 0
grid_hashes[get_hash_grid(grid)] = step
while True:
  step += 1
  grid = get_next_grid(grid)
  grid_hash = get_hash_grid(grid)
  if grid_hash in grid_hashes:
    break
  else:
    grid_hashes[grid_hash] = step

cycle_start = grid_hashes[grid_hash]
print cycle_start, step-cycle_start
