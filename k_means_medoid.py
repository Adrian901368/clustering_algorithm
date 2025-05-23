#'''
#k_means_medoid
import tkinter as tk
import random
import numpy as np

# Function to map value from one range to another
def map_range(value, real_min, real_max, tkinter_min, tkinter_max):
    return ((value - real_min) / (real_max - real_min)) * (tkinter_max - tkinter_min) + tkinter_min

# Function to generate random offset and apply it within bounds
def generate_offset(value, min_value, max_value, offset_min=-100, offset_max=100, margin=20):
    if value < min_value + margin:
        offset_max = min(offset_max, max_value - value - margin)
    elif value > max_value - margin:
        offset_min = max(offset_min, min_value - value + margin)

    offset = random.randint(offset_min, offset_max)
    new_value = value + offset
    return max(min_value + margin, min(max_value - margin, new_value))

# Random color generator
def random_color():
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))

# Euclidean distance function
def distance(point1, point2):
    return np.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

# Function to find the closest centroid
def find_closest_medoids(point, medoids):
    distances = [distance(point, medoid) for medoid in medoids]
    return np.argmin(distances)

# I left this function here because i wanted to show i tried to calculate it in most exact way
#def recalculate_medoids(clusters):
 #   new_medoids = []
 #   for cluster in clusters:
  #      if len(cluster) > 0:
            # Find the point with the minimum total distance to all other points in the cluster
  #          distances_sum = []
    #        for point in cluster:
                #total_distance = np.sum([distance(point, other_point) for other_point in cluster])
                #distances_sum.append(total_distance)
            #min_distance_index = np.argmin(distances_sum)
            #new_medoids.append(cluster[min_distance_index])  # Select the medoid
       # else:
            # Assign a random point if the cluster is empty
           # new_medoid = np.array([random.uniform(-5000, 5000), random.uniform(-5000, 5000)])
           # new_medoids.append(new_medoid)
  #  return new_medoids


# Function to recalculate medoids based on centroids and the closest point
def recalculate_medoids(clusters):
    new_medoids = []
    for cluster in clusters:
        if len(cluster) > 0:
            # Calculate centroid
            centroid = np.mean(cluster, axis=0)

            # Find the point closest to this centroid
            distances = [distance(point, centroid) for point in cluster]
            min_distance_index = np.argmin(distances)

            # Set the closest point as the medoid
            new_medoids.append(cluster[min_distance_index])
        else:
            # If the cluster is empty, add a random point
            new_medoid = np.array([random.uniform(-5000, 5000), random.uniform(-5000, 5000)])
            new_medoids.append(new_medoid)
    return  new_medoids


# Function to evaluate cluster success with original coordinates
def evaluate_cluster_success(clusters, centroids):
    successful_clusters = 0
    for i, points in clusters.items():
        if len(points) > 0:
            avg_distance = np.mean([distance(point, centroids[i]) for point in points])
            print(f"Cluster {i + 1}: Average distance (original coordinates) = {avg_distance:.2f}", end=" ")

            if avg_distance < 500:
                print("- Success")
                successful_clusters += 1
            else:
                print("- Failure")
        else:
            print(f"Cluster {i + 1} has no points.")

    return successful_clusters


# Iterative K-medoids clustering function
def k_medoids_clustering(additional_points, main_points, num_clusters, max_iterations=200):
    # Initialize medoids with the first 20 main points
    initial_medoids = [main_points[f'point_{i}'][:2] for i in range(num_clusters)]

    # If more clusters are needed, add random points
    if num_clusters > 20:
        additional_needed = num_clusters - 20
        all_points = [p[:2] for p in additional_points]  # Use only (x, y) coordinates from additional points
        if additional_needed <= len(all_points):
            initial_medoids += random.sample(all_points, additional_needed)
        else:
            # If there are not enough additional points, generate random points
            while len(initial_medoids) < num_clusters:
                new_medoid = np.array([random.uniform(-5000, 5000), random.uniform(-5000, 5000)])  # Ensure it's 2D
                initial_medoids.append(new_medoid)

    medoids = initial_medoids
    clusters = {i: [] for i in range(num_clusters)}

    for iteration in range(max_iterations):
        # Clear clusters in each iteration
        clusters = {i: [] for i in range(num_clusters)}

        # Assign each point to the closest medoid
        for point in additional_points:
            cluster_index = find_closest_medoids(point[:2], medoids)
            clusters[cluster_index].append(point[:2])

        # Recalculate medoids
        new_medoids = recalculate_medoids([np.array(clusters[i]) for i in range(num_clusters)])

        # Check if medoids have stabilized
        if np.allclose(new_medoids, medoids, atol=0.1):
            print(f"Medoids stabilized after {iteration + 1} iterations")
            break

        medoids = new_medoids

    return medoids, clusters



# Create a tkinter window
root = tk.Tk()
root.title("K-Means Clustering with Canvas")

canvas = tk.Canvas(root, width=900, height=900, bg="white")
canvas.pack()

# Generate 20 random main points (initial points)
main_points = {}
for i in range(20):
    x = random.randint(-4980, 4980)
    y = random.randint(-4980, 4980)
    x_normalized = map_range(x, -5000, 5000, 0, 900)
    y_normalized = map_range(y, -5000, 5000, 0, 900)
    main_points[f'point_{i}'] = (x, y, x_normalized, y_normalized)


additional_points = []


for i in range(40000):
    all_points = list(main_points.values()) + additional_points
    selected_point = random.choice(all_points)
    base_x, base_y, _, _ = selected_point

    new_x = generate_offset(base_x, -5000, 5000, margin=20)
    new_y = generate_offset(base_y, -5000, 5000, margin=20)
    new_x_normalized = map_range(new_x, -5000, 5000, 0, 900)
    new_y_normalized = map_range(new_y, -5000, 5000, 0, 900)

    additional_points.append((new_x, new_y, new_x_normalized, new_y_normalized))


def dynamic_k_medoids_clustering(additional_points, main_points, max_distance=500, max_iterations=200):
    num_clusters = 1

    while True:
        # Run k-means clustering
        medoids, clusters = k_medoids_clustering(additional_points, main_points, num_clusters, max_iterations)

        # Evaluate success: check if all points in each cluster are within max_distance of their centroid
        successful_clusters = evaluate_cluster_success(clusters, medoids)
        total_clusters = len(medoids)

        # Check if all clusters meet the success criterion
        if successful_clusters == total_clusters:
            print(f"All clusters successful with {num_clusters} clusters.")
            root.quit()
            return medoids, clusters

        # Increase number of clusters if criterion not met
        num_clusters += 1
        print(f"Increasing to {num_clusters} clusters...")
# Perform k-means clustering
final_centroids, final_clusters = dynamic_k_medoids_clustering(additional_points, main_points)

# Assign unique colors to each cluster
centroid_colors = [random_color() for _ in final_centroids]

# Draw additional points as colored circles according to their clusters
for i, points in final_clusters.items():
    for point in points:
        new_x_normalized = map_range(point[0], -5000, 5000, 0, 900)
        new_y_normalized = map_range(point[1], -5000, 5000, 0, 900)
        color = centroid_colors[i]  # Use the color of the corresponding centroid
        radius = 2
        canvas.create_oval(new_x_normalized - radius, new_y_normalized - radius,
                           new_x_normalized + radius, new_y_normalized + radius,
                           fill=color, outline=color)



# Draw centroids with a red outline
for i, centroid in enumerate(final_centroids):
    centroid_x_normalized = map_range(centroid[0], -5000, 5000, 0, 900)
    centroid_y_normalized = map_range(centroid[1], -5000, 5000, 0, 900)
    radius = 6
    canvas.create_text(centroid_x_normalized, centroid_y_normalized, text=f"M{i + 1}", font=("Arial", 10), fill="red")
for i, (name, (x, y, x_norm, y_norm)) in enumerate(main_points.items()):
    radius = 5
    canvas.create_oval(x_norm-radius, y_norm-radius,x_norm+radius, y_norm+radius, fill="white", outline="black")

# Evaluate the success of each cluster
successful_clusters = evaluate_cluster_success(final_clusters, final_centroids)

# Calculate and print the percentage of successful clusters
total_clusters = len(final_centroids)
success_percentage = (successful_clusters / total_clusters) * 100
print(f"Percentage of successful clusters: {success_percentage:.2f}%")

# Run the tkinter main loop
root.mainloop()
#'''


