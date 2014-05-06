This problem reeks of "use a spatial datastructure". 
After considering the problem for a while I decided to implement a [k-d tree](http://en.wikipedia.org/wiki/K-d_tree), where each node splits the space along a plane perpendicular to some axis. The data structure allows for O(log n) search of points in space. 

The method I use to build a balanced k-d tree involves sorting the subset of points in the subtree according to the axis being considered at each depth and choosing the median as the node that defines the splitting plane. 

This is quite heavy and there are more efficient methods of doing it (finding the median in O(n)) or approximate ways of finding the point to split the tree at a certain depth. It was efficient enough so I just sorted.

After obtaining the k-d tree of the points required by the query, for each point I get the neighbors in the square of side 2*(radius+500) centered in the point as we know that no object will have a radius larger than 500. This list of points is then tested to see which ones collide. 

After solving the problem it ocurred to me that since we have a lot of information about the (uniform) distribution of the points, it may suffice to define a grid of 500*500 squares and place each point in its own bucket and test collisions among adjacent buckets - i.e. no fancy spatial datastructures =) 
