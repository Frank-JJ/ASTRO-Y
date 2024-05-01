import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression

def read_data(file_path):
    with open(file_path, "r") as file:
        data = file.readlines()
    return data

def parse_data(data):
    time = []
    x_position = []
    y_position = []
    for line in data[2:]:
        parts = line.strip().split(";")
        time.append(float(parts[0]))
        x_position.append(float(parts[1]))
        y_position.append(float(parts[2]))
    return time, x_position, y_position

def subtract_initial_position(x_position, y_position):
    initial_x = x_position[0]
    initial_y = y_position[0]
    x_position = np.array(x_position) - initial_x
    y_position = np.array(y_position) - initial_y
    return x_position, y_position

def calculate_average_speed(time, x_position, y_position):
    total_distance_cm = np.sqrt((x_position[-1] - x_position[0])**2 + (y_position[-1] - y_position[0])**2)
    total_time_seconds = time[-1] - time[0]
    average_speed_cm_per_second = total_distance_cm / total_time_seconds
    return average_speed_cm_per_second

def plot_data_with_slope(time, x_position, y_position):
    plt.figure(figsize=(10, 6))
    plt.plot(time, x_position, label='X-Position')
    plt.plot(time, y_position, label='Y-Position')

    # Fit linear regression models to x and y position data
    reg_x = LinearRegression().fit(np.array(time).reshape(-1, 1), x_position)
    reg_y = LinearRegression().fit(np.array(time).reshape(-1, 1), y_position)

    # Predict values for average lines
    avg_x_position = reg_x.predict(np.array(time).reshape(-1, 1))
    avg_y_position = reg_y.predict(np.array(time).reshape(-1, 1))

    # Plot average lines
    plt.plot(time, avg_x_position, color='r', linestyle='--', label='Average X-Position')
    plt.plot(time, avg_y_position, color='g', linestyle='--', label='Average Y-Position')

    plt.xlabel('Time')
    plt.ylabel('Position')
    plt.title('Position vs Time (Relative to Initial Position)')
    plt.legend()
    plt.grid(True)
    plt.show()

# Paths to data files
file_paths = ["Tail_wag/Wail_wag1.txt", "Tail_wag/Wail_wag2.txt", "Tail_wag/Wail_wag3.txt"]

total_average_speed = 0.0

for file_path in file_paths:
    # Step 1: Read the data
    data = read_data(file_path)

    # Step 2: Parse the data
    time, x_position, y_position = parse_data(data)

    # Step 3: Subtract the initial position
    x_position, y_position = subtract_initial_position(x_position, y_position)

    # Step 4: Calculate the average speed
    average_speed = calculate_average_speed(time, x_position, y_position)

    # Add the average speed to the total
    total_average_speed += average_speed

    # Step 5: Plot the data with slope lines
    plot_data_with_slope(time, x_position, y_position)
    print("Average Speed for", file_path, ":", average_speed, "cm/s")

# Calculate the overall average speed
overall_average_speed = total_average_speed / len(file_paths)
print("Total Average Speed of the 3 files:", overall_average_speed, "cm/s")