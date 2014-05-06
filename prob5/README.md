The solution consists of simulating the [game of life](http://en.wikipedia.org/wiki/Conway's_Game_of_Life) and keeping a dictionary from generated boards to the iteration when they first appeared, so that the period can be computed when a board is repeated.

The boards are represented as 64-bit integers when used as keys in the dictionary.
