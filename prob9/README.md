A road that has maximum speed S km/h and L lanes allows a combined S*L km/h to be covered by cars entering the road.

If we define a graph where each edge is a road and its capacity is S*L, the combined speed of cars as they depart from the source city to Awesomeville is the [maximum flow](http://en.wikipedia.org/wiki/Maximum_flow_problem) of the graph.

A correct implementation of max flow for the given conditions yields the max combined speed F in km/h at which cars can depart from the source city to Awesomeville. Since each car has 4m of length, the space between cars is 1m and the roads are already full of cars, the number of cars travelling to Awesomeville in one hour is F / (0.004 + 0.001) = 200 * F.

*NOTE*: Unfortunately the code provided here has an error (probably in the implementation of max flow which I didn't test) and does not produce the correct output for the first city of the submit phase.
