# STL-Writer-for-Terrain
Writes an ASCII STL file given a grid of height data in ASCII format from Ordinance Survey.
Written to convert OS terrain data into a mesh to conduct wind simulations over terrain. 

For each point in the dataset, two triangular surfaces are generated using the three nearest lower and right-hand neighbours. 

The script assumes that the given ASCII file contains 5 header rows which contain:
* ncols
* nrows
* xllcorner
* yllcorner
* cellsize

xllcorner and yllcorner correspond to the coordinate of the lowest left hand data point.
cellsize corrensonds to the distance between data points. 



