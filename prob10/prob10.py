import urllib
k = raw_input()
f = urllib.urlopen('http://random.contest.tuenti.net/?input=' + k)
s = f.read()
print s

