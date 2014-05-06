t1 = int(raw_input())
t2 = int(raw_input())

parent = {} 
rank = {}

def find(x, parent):
  if parent[x] != x:
    parent[x] = find(parent[x], parent)
  return parent[x]

def union(x, y, parent, rank):
  x_root = find(x, parent)
  y_root = find(y, parent)
  if x_root == y_root:
    return
  if rank[x_root] < rank[y_root]:
    parent[x_root] = y_root
  elif rank[x_root] > rank[y_root]:
    parent[y_root] = x_root
  else:
    parent[y_root] = x_root
    rank[x_root] += rank[x_root]


calls = 0
connected = False
parent[t1] = t1
rank[t1] = 0
parent[t2] = t2
rank[t2] = 0
#old school union-find O(1) per call
for line in open("phone_call.log"):
  id1, id2 = map(int, line.strip().split())
  if id1 not in parent:
    parent[id1] = id1
    rank[id1] = 0
  if id2 not in parent:
    parent[id2] = id2
    rank[id2] = 0
  union(id1, id2, parent, rank)
  if find(t1, parent) == find(t2, parent):
    connected = True
    break
  calls+=1
if connected:
  print "Connected at " + str(calls)
else:
  print "Not connected"



