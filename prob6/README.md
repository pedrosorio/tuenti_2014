This was a very nice problem. Doing a [MITM attack](http://en.wikipedia.org/wiki/Man-in-the-middle_attack). 

A bit of stitching client and server code is sufficient to solve this problem. Act as a regular client with your own request when replacing the client requests, and as the server the client expects when replacing the server responses.
