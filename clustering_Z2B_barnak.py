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
            # Perturb the previous centroid slightly to avoid overlap
            new_centroid = np.array([random.uniform(-5000, 5000), random.uniform(-5000, 5000)])
            new_centroids.append(new_centroid)
    return new_centroids

# Create a tkinter window
root = tk.Tk()
root.title("K-Means Clustering with Canvas")

canvas = tk.Canvas(root, width=900, height=900, bg="white")
canvas.pack()

# Generate 20 random main points (initial centroids)
main_points = {}
centroids = []
for i in range(20):
    x = random.randint(-4980, 4980)
    y = random.randint(-4980, 4980)
    x_normalized = map_range(x, -5000, 5000, 0, 900)
    y_normalized = map_range(y, -5000, 5000, 0, 900)

    main_points[f'point_{i}'] = (x, y, x_normalized, y_normalized)
    centroids.append([x, y])

# List to store additional points
additional_points = []

# Clusters dictionary (index of centroid -> list of points)
clusters = {i: [] for i in range(len(centroids))}

# Generate 400 additional points based on all points (main + additional) and assign to clusters
for i in range(40000):
    all_points = list(main_points.values()) + additional_points
    selected_point = random.choice(all_points)
    base_x, base_y, _, _ = selected_point

    new_x = generate_offset(base_x, -5000, 5000, margin=20)
    new_y = generate_offset(base_y, -5000, 5000, margin=20)

    new_x_normalized = map_range(new_x, -5000, 5000, 0, 900)
    new_y_normalized = map_range(new_y, -5000, 5000, 0, 900)

    # Find the closest centroid and assign the new point to that cluster
    cluster_index = find_closest_centroid([new_x, new_y], centroids)
    clusters[cluster_index].append([new_x, new_y])

    # Store the normalized point without assigning color yet
    additional_points.append((new_x, new_y, new_x_normalized, new_y_normalized))

# Recalculate centroids after all points have been assigned
centroids = recalculate_centroids([np.array(clusters[i]) for i in range(len(centroids))])

# Assign unique colors to each cluster
centroid_colors = [random_color() for _ in centroids]

# Draw additional points as colored circles according to their clusters
for i, points in clusters.items():
    for point in points:
        new_x, new_y = point
        new_x_normalized = map_range(new_x, -5000, 5000, 0, 900)
        new_y_normalized = map_range(new_y, -5000, 5000, 0, 900)
        color = centroid_colors[i]  # Use the color of the corresponding centroid
        radius = 2
        canvas.create_oval(new_x_normalized - radius, new_y_normalized - radius,
                           new_x_normalized + radius, new_y_normalized + radius,
                           fill=color, outline=color)

# Draw the first 20 main points as black circles with "o"
for name, (x, y, x_norm, y_norm) in main_points.items():
    radius = 10
    canvas.create_text(x_norm, y_norm, text="o", font=("Arial", 15), fill="black")

# Run the tkinter loop
root.mainloop()
