from collections import deque, defaultdict
import itertools
import fileinput

inds = {"A": 0, "C": 1, "G": 2, "T": 3}

def compute_hash(dna):
  return sum([inds[dna[i]] * 4**i for i in xrange(len(dna))])

def get_neighbors(dna, seqs_accessible):
  result = []
  hash_val = compute_hash(dna)
  for i in xrange(len(dna)):
    mult = 4**i
    #use rolling hash to make it faster to check whether a neighbor
    #can be visited (exists and hasn't been visited before)
    #in the case of long strings O(1) vs O(string length)
    hash_val -= inds[dna[i]] * mult
    for ind in xrange(4):
      cur_hash = hash_val + ind * mult
      if seqs_accessible[cur_hash]:
        result.append((dna[:i] + "ACGT"[ind] + dna[i+1:], cur_hash))
        seqs_accessible[cur_hash] = False
    hash_val += inds[dna[i]] * mult 
  return result

seqs_accessible = defaultdict(itertools.repeat(False).next)
dna_strings = []
transition_from = {} 

for line in fileinput.input():
  dna_strings.append(line.strip())
  seqs_accessible[compute_hash(line.strip())] = True 

target_hash = compute_hash(dna_strings[1])

#BFS to find the shortest path from start to last
d = deque([(dna_strings[0])])
while d:
  dna = d.pop()
  neighbors = get_neighbors(dna, seqs_accessible)
  for dna_n, hash_code in neighbors:
    transition_from[dna_n] = dna
    if hash_code == target_hash:
      d.clear()
      break
    d.append(dna_n)

#Follow the links back to find the path
path = [dna_strings[1]]
cur = path[0]
while cur != dna_strings[0]:
  cur = transition_from[cur]
  path.append(cur)
print '->'.join(path[::-1])


