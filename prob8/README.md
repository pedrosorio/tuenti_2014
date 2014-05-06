The [15 puzzle](http://en.wikipedia.org/wiki/15_puzzle) similarities biased me towards an [A*](http://en.wikipedia.org/wiki/A*_search_algorithm) approach. I even came up with a clever admissible heuristic, using the manhattan distance:

The largest distance between a person and its goal + (the second largest distance between a person and its goal - 1) + (the third ... - 2) + ...

Where the sequence goes on while the individual terms are positive. This works because we will need to swap the first person the full distance, the second person may get swapped once to be closer to its goal while the first person is moving but will then have to go the rest of the way, the third person may be swapped by the first and second people and get 2 units closer to its goal, etc.

Obviously, in each instance of the problem the names are ignored and the people are assigned numbers allowing the board to be represented by a 9 digit number (i.e. an int) that can be easily hashed and manipulated. Having to use a priority queue for the A* (where updated estimates can not be directly replaced in the priority queue leading to a lot of unnecessary nodes staying around) makes this a bit inefficient. 

A much better solution would have been to precompute the distances from the original position (876543210) to all possible 9! permutations (362880) using BFS and just use those to answer all of the test cases.
