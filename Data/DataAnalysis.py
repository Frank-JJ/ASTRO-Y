import os
import re
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
import pandas as pd

def read_data(file_path):
    with open(file_path, "r") as file:
        data = file.readlines()
    return data

def parse_data(data):
    time = []
    x_position = []
    y_position = []
    for line in data[2:]:
        parts = line.strip().split("\t")
        if len(parts) == 3:  # Ensure all three parts are present
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

def calculate_straightness(x_position, y_position):
    total_displacement_x = abs(x_position[-1] - x_position[0])
    total_displacement_y = abs(y_position[-1] - y_position[0])
    if total_displacement_y == 0:
        return float('inf')
    straightness = total_displacement_x / total_displacement_y
    return straightness

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

# Path to the main folder
main_folder = "Data"

# Iterate through subfolders
for subfolder in os.listdir(main_folder):
    #print(subfolder)
    subfolder_path = os.path.join(main_folder, subfolder)
    
    if os.path.isdir(subfolder_path):
        # Initialize dictionary to store average speeds for each speed in the subfolder
        subfolder_average_speeds = {"05": [], "10": [], "20": []}
        subfolder_average_straightness = {"05": [], "10": [], "20": []}
    

        # Iterate through files in the subfolder
        for file_name in os.listdir(subfolder_path):
            if file_name.endswith(".txt"):
                file_path = os.path.join(subfolder_path, file_name)

                # Extract speed information from file name
                speed_match = re.search(r'plast__left_(\w+)_(\d+)_\d+', file_name)
                #speed_match = re.search(r'plast__right_(\w+)_(\d+)_\d+', file_name)
                #speed_match = re.search(r'wood__left_(\w+)_(\d+)_\d+', file_name)
                #speed_match = re.search(r'wood__right_(\w+)_(\d+)_\d+', file_name)

                if speed_match:
                    speed_type = speed_match.group(1)
                    speed_value = speed_match.group(2)
                    

                    # Step 1: Read the data
                    data = read_data(file_path)
                    

                    # Step 2: Parse the data
                    time, x_position, y_position = parse_data(data)
                    

                    # Step 3: Subtract the initial position
                    x_position, y_position = subtract_initial_position(x_position, y_position)

                    # Step 4: Calculate the average speed
                    average_speed = calculate_average_speed(time, x_position, y_position)
                    subfolder_average_speeds[speed_value].append(average_speed)

                    # Step 5: Calculate the straightness
                    straightness = calculate_straightness(x_position, y_position)
                    subfolder_average_straightness[speed_value].append(straightness)

                    # Step 5: Plot the data with slope lines
                    #plot_data_with_slope(time, x_position, y_position)
                    #print("Average Speed for", file_name, ":", average_speed, "cm/s")

        # Calculate and print the average speed for each speed in the subfolder
        for speed, speeds_list in subfolder_average_speeds.items():
            if speeds_list:
                avg_speed = np.mean(speeds_list)
                std_dev_speed = np.std(speeds_list)
                print("Average Speed for", subfolder, "at", speed, "speed:", avg_speed, "cm/s", "Standard Deviation:", std_dev_speed, "cm/s")

        for speed, speeds_list in subfolder_average_straightness.items():
            if speeds_list:
                avg_straightness = np.mean(speeds_list)
                std_dev_straightness = np.std(speeds_list)
                print("Average Straightness for", subfolder, "at", speed, "speed:", avg_straightness, ", Standard Deviation:", std_dev_straightness)


# End of subfolder iteration