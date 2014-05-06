from math import sqrt

squares = {}

for val in xrange(int(1.5*1337)):
  squares[val**2] = val

N = int(raw_input())
for case in xrange(N):
  x, y = map(int, raw_input().split())
  sq = x**2 + y**2
  if sq in squares:
    print squares[sq]
  else:
    res = round(sqrt(sq), 2)
    print '%.2f' % res
