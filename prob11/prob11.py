from Crypto.Cipher import AES
import string
import fileinput
import heapq
import itertools

#all possible combinations of 3 letters
key_suffixes = [a+b+c for a in string.ascii_letters for b in string.ascii_letters for c in string.ascii_letters]

#read last timestamp of user from files
def get_last_timestamp(user_id):
  with open("last_times/"+user_id[-2:]+"/"+user_id+".timestamp") as f:
    timestamp = f.readline()
  return timestamp.strip()

#open file with encrypted feed for a user
def get_user_encrypted_feed(user_id):
  return open("encrypted/"+user_id[-2:]+"/"+user_id+".feed", "rb")

#return the 32byte key that produces the expected output
#when decrypting the first block of a feed
def return_key(first_block, user_id, timestamp, key_stem):
  tot_len = min(16, len(user_id) + len(timestamp) + 1)
  expected = user_id + " " + timestamp
  expected = expected[:16]
  for suffix in key_suffixes:
    obj = AES.new(key_stem + suffix, AES.MODE_ECB)
    msg = obj.decrypt(first_block)
    if msg[:tot_len] == expected:
      return key_stem + suffix
  return 0

#find the key corresponding to the user
#and return a list of (-timestamp, event_id)
#of all the posts of the user
def get_all_posts(user_info, user_id):
  key_stem, timestamp = user_info[user_id]
  #print key_stem, timestamp, user_id
  feed = get_user_encrypted_feed(user_id)
  first_block = feed.read(16)
  key = return_key(first_block, user_id, timestamp, key_stem)
  obj = AES.new(key, AES.MODE_ECB)
  plaintext = obj.decrypt(first_block + feed.read()).strip().split()
  posts = [(-int(plaintext[i]), plaintext[i+1]) for i in xrange(1,len(plaintext),3)] 
  feed.close()
  return posts

#class inspired by: 
#http://wordaligned.org/articles/merging-sorted-streams-in-python.html
#instead of just returning an iterator to a lazy merge of sorted sequences
#this class allows the user to add new sorted sequences to the global merge
#as well as peek at the top (smallest) element without needing to pop it
#and consume the iterator
class CustomMerge:
  def __init__(self, *sequences):
    self.heap = []
    for seq in sequences:
      iterator = iter(seq)
      for current_value in iterator:
        self.heap.append((current_value, iterator))
        break
    heapq.heapify(self.heap)

  def add_sequence(self, sequence):
    iterator = iter(sequence)
    for current_value in iterator:
      heapq.heappush(self.heap, (current_value, iterator))

  def get_top(self):
    if not self.heap:
      return None
    return self.heap[0][0]

  def pop(self):
    if not self.heap:
      return None
    return_value, iterator = self.heap[0]
    for current_value in iterator:
      heapq.heapreplace(self.heap, (current_value, iterator))
      break
    else:
      heapq.heappop(self.heap)
    return return_value

#return a list of the N most recent event_id given info about the users
#(key_stem and last timestamp)
def recent_events(user_info, N):
  selected_events = []
  #use negative timestamps because python uses min-heap for merge
  recent_users = sorted([(-int(user_info[user_id][1]), user_id) for user_id in user_info], reverse=True)
  #fancy would be to load each user's feed partially as the need arises
  #and mandatory if each user has a lot of posts
  #but since each user has a small number of posts
  #it's easier to just decrypt the whole feed at once
  #when the most recent timestamp for a user is more recent than any
  #other candidate posts
  posts = get_all_posts(user_info, recent_users.pop()[1])
  posts_sorted = CustomMerge(posts)
  while len(selected_events) < N:
    next_post = posts_sorted.get_top()
    #keep looping while we need more events and there are posts in the heap
    #that have a timestamp more recent than the most recent timestamp of any
    #of the unread users
    while len(selected_events) < N and next_post != None and (not recent_users or next_post[0] < recent_users[-1][0]):
      selected_events.append(next_post[1])
      posts_sorted.pop()
      next_post = posts_sorted.get_top()
    if len(selected_events) == N:
      break
    #when some of the conditions above does not hold, read the next user
    #with the most recent timestamp
    if recent_users:
      posts_sorted.add_sequence(get_all_posts(user_info, recent_users.pop()[1]))
    else: 
      break
  return selected_events 

for line in fileinput.input():
  data = line.strip().split("; ")
  N = int(data[0])
  user_info = {}
  for user_data in data[1:]:
    user_id, key_stem = user_data.split(",")
    timestamp = get_last_timestamp(user_id)
    user_info[user_id] = [key_stem, timestamp]
  print " ".join(recent_events(user_info, N))
