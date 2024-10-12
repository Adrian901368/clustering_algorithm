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
def find_closest_centroid(point, centroids):
    distances = [distance(point, centroid) for centroid in centroids]
    return np.argmin(distances)

# Function to recalculate centroids as the mean of points in each cluster
def recalculate_centroids(clusters):
    new_centroids = []
    for cluster in clusters:
        if len(cluster) > 0:
            new_centroid = np.mean(cluster, axis=0)
            new_centroids.append(new_centroid)
        else:
            new_centroid = np.array([random.uniform(-5000, 5000), random.uniform(-5000, 5000)])
            new_centroids.append(new_centroid)
    return new_centroids

# Function to evaluate cluster success
def evaluate_cluster_success(clusters, centroids):
    successful_clusters = 0
    for i, points in clusters.items():
        if len(points) > 0:
            avg_distance = np.mean([distance(point, centroids[i]) for point in points])

            print(f"Cluster {i+1}: Average distance = {avg_distance:.2f}", end=" ")
            if avg_distance < 500:
                print("- Success")
                successful_clusters += 1
            else:
                print("- Failure")
    return successful_clusters

# Iterative K-means clustering function
def k_means_clustering(additional_points, main_points, max_iterations=20):
    centroids = [list(p[:2]) for p in main_points.values()]  # Start with initial centroids
    clusters = {i: [] for i in range(len(centroids))}

    for iteration in range(max_iterations):
        # Clear clusters in each iteration
        clusters = {i: [] for i in range(len(centroids))}

        # Assign each point to the closest centroid
        for point in additional_points:
            cluster_index = find_closest_centroid(point[:2], centroids)
            clusters[cluster_index].append(point[:2])

        # Recalculate centroids
        new_centroids = recalculate_centroids([np.array(clusters[i]) for i in range(len(centroids))])

        # Check if centroids have stabilized (no significant change)
        if np.allclose(new_centroids, centroids, atol=0.1):
            print(f"Centroids stabilized after {iteration + 1} iterations")
            break

        centroids = new_centroids

    return centroids, clusters

# Create a tkinter window
root = tk.Tk()
root.title("K-Means Clustering with Canvas")

canvas = tk.Canvas(root, width=900, height=900, bg="white")
canvas.pack()

# Generate 20 random main points (initial centroids)
main_points = {}
for i in range(20):
    x = random.randint(-4980, 4980)
    y = random.randint(-4980, 4980)
    x_normalized = map_range(x, -5000, 5000, 0, 900)
    y_normalized = map_range(y, -5000, 5000, 0, 900)
    main_points[f'point_{i}'] = (x, y, x_normalized, y_normalized)

# List to store additional points
additional_points = []

# Generate 400 additional points based on all points (main + additional) and assign to clusters
for i in range(40000):
    all_points = list(main_points.values()) + additional_points
    selected_point = random.choice(all_points)
    base_x, base_y, _, _ = selected_point

    new_x = generate_offset(base_x, -5000, 5000, margin=20)
    new_y = generate_offset(base_y, -5000, 5000, margin=20)
    new_x_normalized = map_range(new_x, -5000, 5000, 0, 900)
    new_y_normalized = map_range(new_y, -5000, 5000, 0, 900)

    additional_points.append((new_x, new_y, new_x_normalized, new_y_normalized))

# Perform k-means clustering
final_centroids, final_clusters = k_means_clustering(additional_points, main_points)

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

# Draw the first 20 main points as black circles with "o N"
for i, (name, (x, y, x_norm, y_norm)) in enumerate(main_points.items()):
    radius = 10
    canvas.create_text(x_norm, y_norm, text=f"o{i+1}", font=("Arial", 15), fill="black")

# Evaluate the success of each cluster
successful_clusters = evaluate_cluster_success(final_clusters, final_centroids)

# Calculate and print the percentage of successful clusters
total_clusters = len(final_centroids)
success_percentage = (successful_clusters / total_clusters) * 100
print(f"Percentage of successful clusters: {success_percentage:.2f}%")

# Run the tkinter loop
root.mainloop()
