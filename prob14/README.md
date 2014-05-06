An interesting problem. The multiple trains/routes makes it not obvious.
Since the limits were quite low I decided to attempt a backtracking approach with some techniques to limit the branching:
* Always try to move a train several times in a row - only consider moving the other train if the current one has run out of fuel or has just brought a wagon to a station that is shared by both networks - this avoids exploring permutations of moves that are equivalent
* Never let the same wagon visit the same station twice
* Build the all-pairs graph for each network using ~~Ford-Fulkerson~~ Floyd-Warshall (I always swap these two names...)  before beginning and allow a train to move/carry a wagon directly to any station in a network. Then, forbid a train from carrying the same wagon/moving without a wagon twice in a row.

All of the above help in some way, but ensuring that the search terminates early when there is obviously no hope of beating the best value found so far is essential. In order to do that:
* Before starting, build the all-pairs graph for the full map and precompute an array of wagons in descending order of values, with the corresponding distances to their destinations. 
* Everytime a wagon is moved, update the distance (O(1) lookup in the all-pairs graph) in the array. If a wagon is delivered to the destination, replace its value with 0 in the array.
* At every step of the algorithm, compute an upper bound for the value that may be obtained in this branch by solving the [continuous knapsack problem](http://en.wikipedia.org/wiki/Continuous_knapsack_problem) where the item values and weight are the values and distances in the array of wagons, respectively, and the knapsack capacity is the sum of fuel in the two trains. Since the array of wagons is sorted by value this can be computed in O(#wagons).

Obviously the above upper bound is quite loose as it doesn't take into account the position of the trains, and the interactions in the positions of the wagons and even the knapsack problem is relaxed compared to the 0-1 version which would be a tighter upper bound (but harder to compute).

Still, computing the upper bound as defined above prunes a lot of branches that are hopeless and makes this quite efficient. It should also be noted that the algorithm works for any number of networks as is.
