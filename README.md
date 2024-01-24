# HAC
hierarchical agglomerative clustering
This project performs the HAC complete linkage algorithm on a CSV file containing a list of countries, and their socio economic data such as GDP, Literacy, Infant mortality, and phones per 1000, etc. In total 6 parameters are taken into consideration.
Each country is represented by a 6 dimensional feature vector. 
The hac(features) function works similarly to the scipy.cluster.heirarchy.linkage() with method='complete'
The distance function used is the standard euclidean distance function.
The project also is able to create a matplotlib figure that visualizes the clustering algorithm at each iteration. 
Other information:
the program has a dynamic programming approach, utilizing a square matrice, which starts with dimensions n*n where each M[i][j] stores the distance between cluster i and cluster
After each iteration of the clustering algorithm, two clusters are merged, the corresponding rows and columns for those clusters in the matrice are all set to 0( indicating that these are not mergable in further iterations. 
The newly created cluster is added to the matrice by appending a row and a column. 
The values for the distance between the newly created cluster and other clusters is determined by taking the max value of the distance between those clusters and the two clusters that were merged to create the new cluster. 
At each iteration, we select the lowest non zero value in the matrice to find the two clusters that will be merged at that iteration.
