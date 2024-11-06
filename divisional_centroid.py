#'''
#divisional_centroid
import tkinter as tk
import random
import numpy as np

def map_range(value, real_min, real_max, tkinter_min, tkinter_max):
    return ((value - real_min) / (real_max - real_min)) * (tkinter_max - tkinter_min) + tkinter_min

def generate_offset(value, min_value, max_value, offset_min=-100, offset_max=100, margin=20):
    if value < min_value + margin:
        offset_max = min(offset_max, max_value - value - margin)
    elif value > max_value - margin:
        offset_min = max(offset_min, min_value - value + margin)
    offset = random.randint(offset_min, offset_max)
    new_value = value + offset
    return max(min_value + margin, min(max_value - margin, new_value))

def random_color():
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))

def distance(point1, point2):
    return np.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

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

def split_cluster(cluster):
    if len(cluster) < 2:
        return [cluster]
    centroids = random.sample(cluster, 2)
    clusters = {0: [], 1: []}
    for point in cluster:
        distances = [distance(point, centroid) for centroid in centroids]
        closest_centroid = np.argmin(distances)
        clusters[closest_centroid].append(point)
    return [clusters[0], clusters[1]]

def evaluate_cluster_success(clusters, centroids):
    successful_clusters = 0
    for i, points in enumerate(clusters):
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
    return successful_clusters == len(clusters)

def divisive_clustering(points):
    clusters = [points]
    while True:
        print(f"Trying with {len(clusters)} clusters")  # Print current number of clusters
        centroids = recalculate_centroids(clusters)
        if evaluate_cluster_success(clusters, centroids):
            print(f"Successful clustering achieved with {len(clusters)} clusters\nsuccesful rate 100%")
            draw_clusters(clusters, centroids)  # Draw only the successful clusters
            break

        # Split the largest cluster
        cluster_to_split_index = max(range(len(clusters)), key=lambda i: np.mean([distance(point, centroids[i]) for point in clusters[i]]))
        largest_cluster = clusters[cluster_to_split_index]
        if len(largest_cluster) <= 1:
            break
        new_clusters = split_cluster(largest_cluster)
        clusters.pop(cluster_to_split_index)
        clusters.extend(new_clusters)

def draw_clusters(clusters, centroids):
    canvas.delete("all")
    colors = [random_color() for _ in range(len(clusters))]
    for i, points in enumerate(clusters):
        for point in points:
            x_normalized = map_range(point[0], -5000, 5000, 0, 900)
            y_normalized = map_range(point[1], -5000, 5000, 0, 900)
            canvas.create_oval(x_normalized - 2, y_normalized - 2, x_normalized + 2, y_normalized + 2, fill=colors[i], outline=colors[i])

    for i, centroid in enumerate(centroids):
        x_normalized = map_range(centroid[0], -5000, 5000, 0, 900)
        y_normalized = map_range(centroid[1], -5000, 5000, 0, 900)
        canvas.create_oval(x_normalized - 3, y_normalized - 3, x_normalized + 3, y_normalized + 3, fill=colors[i], outline="black")
        canvas.create_text(x_normalized, y_normalized, text=f"C{i + 1}", font=("Arial", 10), fill="black")
    root.update()

root = tk.Tk()
root.title("Divisive Clustering with Canvas")
canvas = tk.Canvas(root, width=900, height=900, bg="white")
canvas.pack()

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

divisive_clustering(additional_points)
root.mainloop()
#'''