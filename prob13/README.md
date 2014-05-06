After seeing all the hints about "timing" and "side channels" and experimenting with the alternative mode hinted at in the html which returned the server processing time, it became obvious that the password could be obtained by correlating inputs with the server response times.

My first approach tried all ascii characters and proceeded with any that had a signficant (larger than 50 percent of the average) response time, trying to add a new character and so on. It soon became apparent that all the characters where hexadecimal digits and after some fiddling that a single character made the response time significantly larger at each length.

Since I had no way of determining a lower bound for the increase in processing time provoked by the "correct" character at each length, I decided to ditch the "early termination" approach where a character would be chosen immediately if the processing time was significant 1.xx times the one for the same string without that character. 

After that I decided to keep it safe in the submit phase and test all [0-f] at each length and pick the one with largest processing time. This made it a bit slower and since the approach was network bound I added 16 threads to make all the requests at a certain length parallel. 
