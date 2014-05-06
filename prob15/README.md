An interesting challenge. This one was done without any fancy approaches. Use two 64-bit boards to represent the location of the white pieces and black pieces.

Define a utility function that given the two boards and a position return another 64-bit board corresponding to the flipped positions. If this board is 0 the move is illegal, otherwise it can be ORed with the board that made the move to add the pieces and AND-NOTed with the other player's board to remove the pieces. 

Apart from the bit trickery the approach is quite simple: pass to a utility function the two boards, whether the "challenge player" is currently moving and the number of moves allowed before a piece has to be in the corner. This function will test all possible moves using the approach mentioned above and recursively call itself swapping the boards and decrementing the number of available moves as required.

The above function has two different behaviors depending on whose turn it is:
* If the "challenge player" is moving and after calling itself with the boards resulting from some move, the return value is positive, the function returns immediately a positive integer that represents the move that was done. If no such move can be found (including skipping if there are no moves available), the function returns 0.
* If the "other player" is moving and after calling itself with the boards resulting from some move, the return value is zero, the function returns 0 immediately. If no such move can be found (including skipping if there are no moves available), the function returns the positive value from the last call.

This ensures that each player only explores options until there is a move that forces the result they want (put in the corner for the "challenge player", avoid a corner piece in the next X moves for the other player).

Another "optimization" that I suppose may help but haven't actually tested is that the players consider the moves in the order of value of the positions in Othello. Since we are interested in the results when both play optimally, this probably leads to pruning more branches than choosing the moves in a random order - most relevant: both players attempt to place pieces in the corner first and to place pieces adjacent to corners last.
