import os
import re
import matplotlib.pyplot as plt
import matplotlib
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

data_dict = {}

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
                speed_match = re.search(r'(\w+)__(\w+)_(\w+)_(\d+)_(\d+)', file_name)
                # speed_match = re.search(r'plast__left_(\w+)_(\d+)_\d+', file_name)
                # speed_match = re.search(r'plast__right_(\w+)_(\d+)_\d+', file_name)
                # speed_match = re.search(r'wood__left_(\w+)_(\d+)_\d+', file_name)
                # speed_match = re.search(r'wood__right_(\w+)_(\d+)_\d+', file_name)
                
                if speed_match:
                    # print("here", speed_match.group(1))
                    speed_type = speed_match.group(3)
                    speed_value = speed_match.group(4)
                    

                    # Step 1: Read the data
                    data = read_data(file_path)
                    

                    # Step 2: Parse the data
                    time, x_position, y_position = parse_data(data)

                    column_names = file_name.split(".")[0]
                    
                    # print("column names:", column_names)
                    # new_data_frame = pd.DataFrame(values)
                    # data_frame = pd.concat([data_frame, new_data_frame], ignore_index=False, axis=1)
                    

                    # Step 3: Subtract the initial position
                    x_position, y_position = subtract_initial_position(x_position, y_position)

                    # Step 4: Calculate the average speed
                    average_speed = calculate_average_speed(time, x_position, y_position)
                    subfolder_average_speeds[speed_value].append(average_speed)

                    # Step 5: Calculate the straightness
                    straightness = calculate_straightness(x_position, y_position)
                    subfolder_average_straightness[speed_value].append(straightness)

                    if x_position[-1] < 0:
                        print("Fucked in", column_names)

                    values = {"time" : time, 
                              "x_position" : x_position, 
                              "y_position" : y_position,
                              "average_speed" : average_speed,
                              "straightness" : straightness}

                    if speed_match.group(1) not in data_dict:
                        data_dict[speed_match.group(1)] = {}
                    if speed_match.group(2) not in data_dict[speed_match.group(1)]:
                        data_dict[speed_match.group(1)][speed_match.group(2)] = {}
                    if speed_match.group(3) not in data_dict[speed_match.group(1)][speed_match.group(2)]:
                        data_dict[speed_match.group(1)][speed_match.group(2)][speed_match.group(3)] = {}
                    if speed_match.group(4) not in data_dict[speed_match.group(1)][speed_match.group(2)][speed_match.group(3)]:
                        data_dict[speed_match.group(1)][speed_match.group(2)][speed_match.group(3)][speed_match.group(4)] = {}
                    if speed_match.group(4) not in data_dict[speed_match.group(1)][speed_match.group(2)][speed_match.group(3)]:
                        data_dict[speed_match.group(1)][speed_match.group(2)][speed_match.group(3)][speed_match.group(4)] = {}
                    data_dict[speed_match.group(1)][speed_match.group(2)][speed_match.group(3)][speed_match.group(4)][speed_match.group(5)] = values


                    # Step 5: Plot the data with slope lines
                    #plot_data_with_slope(time, x_position, y_position)
                    #print("Average Speed for", file_name, ":", average_speed, "cm/s")

        # Calculate and print the average speed for each speed in the subfolder
        # for speed, speeds_list in subfolder_average_speeds.items():
        #     if speeds_list:
        #         avg_speed = np.mean(speeds_list)
        #         std_dev_speed = np.std(speeds_list)
        #         print("Average Speed for", subfolder, "at", speed, "speed:", avg_speed, "cm/s", "Standard Deviation:", std_dev_speed, "cm/s")

        # for speed, speeds_list in subfolder_average_straightness.items():
        #     if speeds_list:
        #         avg_straightness = np.mean(speeds_list)
        #         std_dev_straightness = np.std(speeds_list)
        #         print("Average Straightness for", subfolder, "at", speed, "speed:", avg_straightness, ", Standard Deviation:", std_dev_straightness)


# End of subfolder iteration

# print(pd.DataFrame(data_dict))

data_frame = pd.DataFrame(data_dict)

print(data_frame)

plast_data = data_frame["plast"]

print("\n")
# print(plast_data["left"]["crawl"]["05"].items())

# print("\n")
# print(plast_data[0])
# print(data_frame["plast"]["left"]["crawl"]["05"]["3"])

f, axs = plt.subplots(figsize=(10, 6))
surface = "plast"
direction = "left"
gait = "crawl"
# key = "3"
speed_colors = ["r","y","b"]
test_lines = ['-','--',':']
test_markers = [' ',' ',' ']
test_width = [3,3,3]
for speed_index, key_speed in enumerate(data_frame[surface][direction][gait].keys()):
    # speed_distances = {}
    for test_index, (key_test, value) in enumerate(data_frame[surface][direction][gait][key_speed].items()):
        time = value["time"]
        x_position = value["x_position"]
        y_position = value["y_position"]
        distance = np.sqrt(x_position**2 + y_position**2)
        # print("\ntime:", time)
        # print("\ndistance:", distance)
        # for index, second in enumerate(time):
        #     if second not in speed_distances:
        #         speed_distances[second] = 0
        #         print("not same in: ", key_speed, key_test, second)
        #     speed_distances[second] = ((speed_distances[second]*test_index) + distance[index]) / (test_index + 1)
        # plt.plot(time, x_position, label=f"{key} x", linewidth=4)
        # plt.plot(time, y_position, label=f"{key} y", linewidth=4)
        plt.plot(time, distance, label=f"cycle-time[s]:{int(key_speed)/10}", linewidth=test_width[test_index], markersize=test_width[test_index], color=speed_colors[speed_index], linestyle=test_lines[test_index], marker=test_markers[test_index])

    # test_index = 0
    # times = speed_distances.keys()
    # # print(times)
    # distances = speed_distances.values()
    # plt.plot(times, distances, label=f"cycle-time[s]:{int(key_speed)/10}", linewidth=test_width[test_index], markersize=test_width[test_index], color=speed_colors[speed_index], linestyle=test_lines[test_index], marker=test_markers[test_index])


plt.xlabel('Time')
plt.ylabel('Position')
plt.title(f'Position vs Time (Relative to Initial Position) {surface}+{direction}+{gait}')
h, l = axs.get_legend_handles_labels()
# plt.legend()
plt.legend(handles=zip(h[::3], h[1::3]), labels=l[::3], handler_map = {tuple: matplotlib.legend_handler.HandlerTuple(None)})
plt.grid(True)
plt.show()

# data_frame = data_frame.transpose()

# print(data_frame[data_frame.columns[0]])