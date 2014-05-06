For this problem we need to reconstruct the keys that were used to encrypt the events of each user and then for a list of users return the aggregate N most recent events.

Since we are given 29 bytes of each key, we know the format of the files and the complete key only has Latin alphabet letters, for any given user it suffices to attempt all possible (52^3 = 140608) keys on the first 16-byte block of the encrypted file and compare the plaintext with the expected information (we know the userid and the most recent timestamp for the user should be in the first block).

Since each request may contain up to 3000 users but requires at most 300 events, it's obviously nonsensical to perform the brute-force key finding process for all of them. After sorting the users by most recent timestamp, and while we don't have the N most recent events, the procedure is as follows:

* If we haven't deciphered any events that are more recent than the most recent timestamp of the next user, find the user's key, decipher his posts and add them sorted by timestamp (good thing that's already the case) to kind of priority queue.
* Otherwise, remove the first event from the priority queue and store it in the list of events to be returned.

The way the most recent events are stored and pulled from the queue is based on python's [heapq.merge](https://docs.python.org/2/library/heapq.html#heapq.merge) which doesn't place all of the events in priority queue (which would make it unnecessarily large with many events that are too old to ever be picked out of it) but instead receives sorted lists and returns an iterator. 

The implementation uses a priority queue underneath where an element from a list is added to the priority queue only when the previous element from that list is removed from the priority queue through clever iterator tricks (thus the priority queue never has more elements than the number of lists and a lot of computation is saved) - read about it [here](http://wordaligned.org/articles/merging-sorted-streams-in-python.html). 

I implemented something inspired by this approach but where new source lists can be added to the structure after construction (necessary since we only obtain users' events as the need arises in order to avoid the heavy key recovery process).

The only thing left to say is that I completely forgot that different feeds might require events from the same user. At the very least after the key for a user is recovered it should be stored and perhaps it would be useful to maintain a cache holding the K most recent events for the M most recent users accessed (i.e. typical computation/memory tradeoff).
