A dictionary is maintained with the DNA sequences that can be accessed. The default value of the dictionary is False, and the input determines the sequences that can be accessed. 

The key to the dictionary is the [base-4](http://en.wikipedia.org/wiki/Quaternary_numeral_system) number represented by the DNA sequence. This makes it a lot faster to lookup a sequence with a single different nucleotide in the dictionary (just need to sum and subtract an integer from the previous hash in O(1), instead of generating a new string and using it to make a lookup O(len(sequence))).

The rest of the solution is a simple BFS from source sequence keeping back-links to trace the path.
