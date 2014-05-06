import urllib

data = urllib.urlencode([('input[]', '[]')])
f = urllib.urlopen('http://random.contest.tuenti.net/',data)
s = f.read()
print s
