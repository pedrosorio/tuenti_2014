from collections import defaultdict

phone_list = defaultdict(list)
for line in open("students"):
  separator_index = line.find(",")
  name = line[:separator_index]
  key = line[separator_index+1:].strip()
  phone_list[key].append(name)

T = int(raw_input())
for test in xrange(1,T+1):
  key = raw_input()
  names = phone_list[key]
  if len(names) == 0:
    res = "NONE"
  else:
    res = ",".join(sorted(names))
  print "Case #" + str(test) + ": " + res

