The problem asks to build a "network" based on the recorded calls and determine the first call when two phone numbers first become "connected" in the network.

This screams [union-find algorithm](http://en.wikipedia.org/wiki/Disjoint-set_data_structure). Implementing it using union by rank and path compression makes for a very efficient solution, where we return the number of the first call where the two numbers are in the same set.
