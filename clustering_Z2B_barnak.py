import tkinter as tk
import random
import numpy as np

# Function to map value from one range to another
def map_range(value, real_min, real_max, tkinter_min, tkinter_max):
    mapped_value = ((value - real_min) / (real_max - real_min)) * (tkinter_max - tkinter_min) + tkinter_min
    return mapped_value

# Function to generate random offset and apply it within bounds
def generate_offset(value, min_value, max_value, offset_min=-100, offset_max=100, margin=20):
    offset = random.randint(offset_min, offset_max)
    new_value = value + offset
    # Clamp the new value to be within the specified bounds while considering the margin
    return max(min_value + margin, min(max_value - margin, new_value))

# Function to generate random color
def random_color():
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))

# Function to find the closest main point color
def closest_color(main_points, new_point):
    min_distance = float('inf')
    closest_color = None
    for (x, y, x_normalized, y_normalized, color) in main_points.values():
        distance = np.sqrt((new_point[0] - x) ** 2 + (new_point[1] - y) ** 2)
        if distance < min_distance:
            min_distance = distance
            closest_color = color
    return closest_color

# Create a tkinter window
root = tk.Tk()
root.title("Random Points with Clusters on Canvas")

# Canvas size 1000x1000
canvas = tk.Canvas(root, width=900, height=900, bg="white")
canvas.pack()

# Generate 20 random main points between -5000 and 5000 with unique colors
main_points = {}
for i in range(1, 21):
    # Generate random coordinates, considering a margin of 20
    x = random.randint(-4980, 4980)  # Adjust bounds to ensure at least 20 margin
    y = random.randint(-4980, 4980)  # Adjust bounds to ensure at least 20 margin

    # Normalize coordinates for the canvas
    x_normalized = map_range(x, -5000, 5000, 0, 900)
    y_normalized = map_range(y, -5000, 5000, 0, 900)

    # Assign each point a unique color
    color = random_color()
    main_points[f'point_{i}'] = (x, y, x_normalized, y_normalized, color)

# List to store additional points
additional_points = []

# Generate 400 additional points based on all points (including main points)
for i in range(1, 8001):
    # Randomly select any point from all previously created points (main + additional)
    all_points = list(main_points.values()) + additional_points
    selected_point = random.choice(all_points)
    base_x, base_y, _, _, _ = selected_point

    # Generate new point with random offsets within bounds
    new_x = generate_offset(base_x, -5000, 5000, margin=20)
    new_y = generate_offset(base_y, -5000, 5000, margin=20)

    # Normalize for canvas (make sure they fit within [0, 1000])
    new_x_normalized = map_range(new_x, -5000, 5000, 0, 900)
    new_y_normalized = map_range(new_y, -5000, 5000, 0, 900)

    # Find the color of the nearest main point
    new_color = closest_color(main_points, (new_x, new_y))

    # Store additional points with their coordinates and colors
    additional_points.append((new_x, new_y, new_x_normalized, new_y_normalized, new_color))

# Draw additional points as colored circles
for point in additional_points:  # Updated to unpack correctly
    new_x_normalized, new_y_normalized, color = point[2], point[3], point[4]  # Unpack correctly
    radius = 2  # Adjust radius for additional points
    canvas.create_oval(new_x_normalized - radius, new_y_normalized - radius,
                       new_x_normalized + radius, new_y_normalized + radius,
                       fill=color, outline=color)

# Draw the first 20 main points as black circles with "o"
for name, (x, y, x_norm, y_norm, color) in main_points.items():
    radius = 10  # You can adjust the radius as needed
    canvas.create_text(x_norm, y_norm, text="o", font=("Arial", 15), fill="black")

# Run the tkinter loop
root.mainloop()
