# MRTStationDistance
This code uses the OneMap API to fetch and compile shortest distance by rail between two stations.

Required:
1) A OneMAP API key, which should be inserted at accessKey near the start of the code
2) A list of station codes and names, which have been attached in this repo for convenience. 

The first part of this code takes the list of station codes and names, and tacks on a Lat/Lon pair. The file is saved as stationGPS.txt.
Assuming that the coordinates of a station are time-invariant, this file need only be generated once and this section of code truncated.

The second part of this code takes every Station GPS pair and runs it through the OneMap routing service, which in turn polls Google Map's service. The mode is set to TRANSIT. The time and date of transit is assumed by this code to be 2019-02-22 at 1200h.
This API returns up to three "itineraries"; the last part of the code iterates over these itineraries to find which the shortest is, by summing the legs within the itineraries and comparing the sum.


Simplifying assumptions:
- Transit returns shortest distance by rail. Strongest assumption - it may be possible, though extremely unlikely, that alternative transport methods (i.e., bus), would return a distance shorter than by rail.

- Distance between stations is time-invariant. This is likely to be true; however, in the event of unforseen circumstances at the chosen transit time, Google may route users via longer routes. 

- Distance between stations is commutative; i.e., distance from A-B == distance from B-A. This lowers computation time by allowing the inner iterator to start only from the outer iterator rather than the start of the list. 
