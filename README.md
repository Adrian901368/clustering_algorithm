Task Z2B – Clustering
Introduction
In this project, I implemented a simulation that uses the k-means algorithm to divide a space into k clusters as optimally as possible for 40,000 points. The goal is to form efficient clusters where the average distance of points from the center is less than 500 in all clusters. I used three types of clustering: k-means with the center as the centroid, k-means with the center as the medoid, and divisive clustering, where the center is the centroid.

Program Algorithm
At the beginning, 20 random points are generated. Around these, an additional 40,000 random points are created. The points are then divided into clusters, for which centers are calculated, and success is measured based on the average distance — which should be less than 500 from the center. Clustering starts with just one cluster, and the program reruns with an increasing number of clusters until the clustering is successful. Once clustering is successful, the result is displayed on a canvas using Tkinter. Clusters are colored according to the cluster they belong to. Each cluster has the same color as its centroid. The original 20 main points are shown in white, and centroids or medoids are labeled as “C{number}” or “M{number}” for better visualization.

Functions in k_means_centroid.py
map_range: Projects actual coordinates onto the Tkinter canvas since the screen resolution is not large enough.

generate_offset: Randomly generates points around the main points with a maximum offset of 100, ensuring they don’t go beyond the canvas boundaries.

random_color: Generates a random color for the points.

distance: Calculates distance.

find_closest_centroid: Finds the nearest centroid for each point.

recalculate_centroids: Recalculates the centroid by taking the average position of points in the cluster. If a cluster is empty, a random point is chosen.

evaluate_cluster_success: Calculates distances of points from the center and computes the average distance for each cluster as well as the number of successful clusters. Then it prints the average distances and success to the console.

k_means_clustering: The main function that initializes all points. Centroids are chosen randomly from the 20 main points. If there are more clusters, additional ones are chosen randomly. Points are assigned to the nearest centroid and colored accordingly. Centroids are recalculated, and if they stabilize (no movement), the output is shown.

dynamic_k_means_clustering: Repeatedly calls k_means_clustering, increasing the number of clusters until successful clustering is achieved.

In the main function, points are generated, coordinates are mapped, the k-means function is called, colors are assigned, and the results are drawn on the canvas. Console output shows cluster success.

Functions in k_means_medoid.py
map_range: Maps real coordinates to Tkinter canvas.

generate_offset: Randomly generates points near the main ones, keeping them within the canvas boundaries.

random_color: Generates a random color.

distance: Calculates distance.

find_closest_medoid: Finds the nearest medoid for each point.

recalculate_medoids: Calculates the centroid and picks the point closest to it as the new medoid. Originally, the function computed the total distance from all points and selected the one with the smallest sum as the new medoid, but this was too time-consuming, taking several hours.

evaluate_cluster_success: Calculates the distances of points to the center and the average distance for each cluster, then prints the results.

k_medoids_clustering: Initializes all points. Medoids are randomly selected from the 20 main points. If there are more clusters, additional ones are randomly chosen. Points are assigned to their closest medoid and colored. Medoids are recalculated and, once stabilized, results are shown.

dynamic_k_medoids_clustering: Calls k_medoids_clustering with an increasing number of clusters until successful clustering is reached.

In main, the program generates points, maps coordinates, runs the k_means function, assigns colors, and outputs results to the console.

Functions in divisional_centroid.py
map_range: Converts actual coordinates to Tkinter canvas coordinates.

generate_offset: Ensures points are generated randomly but only around the main points.

random_color: Generates a random color for points.

distance: Computes the distance.

find_closest_centroid: Finds the nearest centroid for each point.

recalculate_centroids: Determines the center of a cluster. If a cluster is empty, a random point is selected.

split_cluster: Splits the largest cluster into two, assigns new centroids, and redistributes the points.

evaluate_cluster_success: Calculates distances from the center, average distance for each cluster, and the percentage of successful clusters.

divisive_clustering: Splits the largest cluster into two and computes new centroids for the new clusters.

draw_clusters: Draws the points according to the cluster they belong to.

In main, the program generates the points, maps coordinates, runs the k_means function, assigns colors, draws the clusters using draw_clusters, and prints successful clusters to the console.
