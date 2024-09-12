
# UPI Python Docker & ROS Integration

This project automates the setup and execution of Docker containers for running **ROS (Robot Operating System)** nodes and recording ROS topics using `rosbag`. It includes a Python script that calls a shell script (`run.sh`) to start a Docker container, run ROS nodes, and capture the container ID for further operations.

## Features
- Automatically starts a Docker container with ROS Noetic and launches a RealSense camera node.
- Records all ROS topics into a ROS bag file (`rosbag`).
- Captures and outputs the Docker container ID for further management.
- Python integration for ease of use and automation.

## Prerequisites

### Install Docker
Ensure that Docker is installed on your system. You can install Docker by following the official [Docker installation guide](https://docs.docker.com/get-docker/).

### Install ROS Noetic Docker Image
Ensure that you have the `ros:noetic-desktop-full` image available on your machine. You can pull it using:

```bash
docker pull ros:noetic-desktop-full
```

### Python Dependencies
Make sure you have Python 3 installed on your system. The `subprocess` module is used to run shell scripts from Python, which is part of the standard library, so no additional dependencies are required.

## Project Structure
```
upi_python/upi_info_display/
│
├── run.sh                    # Shell script to run the Docker container and launch ROS nodes
├── docker_record_test.py      # Python script that calls run.sh and retrieves the Docker container ID
└── README.md                  # Project documentation
```

## Usage

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/upi_python/upi_info_display.git
cd upi_python/upi_info_display
```

### 2. Make `run.sh` executable
Before running the project, ensure that the `run.sh` script has the appropriate execute permissions:

```bash
chmod +x run.sh
```

### 3. Running the project



#### Running via Python script
Alternatively, you can use the Python script (`docker_record_test.py`) to automate the process:

```bash
python3 docker_record_test.py
```

This will:
- Execute `run.sh`.
- Capture and print the Docker container ID for further use.

### 4. Stopping the Docker container
The container is run with the `--rm` flag, meaning it will automatically be removed after the task completes. You can manually stop the container if needed by using:

```bash
docker stop <container_id>
```

## Example Output

When you run the Python script, you should see output like this:

```bash
Long press detected. Running roslaunch in Docker
Docker container ID: abcdef123456
```

This indicates that the ROS nodes have been successfully launched in a Docker container, and the container ID is `abcdef123456`.

## Troubleshooting

1. **Permission Denied on `run.sh`:**
   - Ensure that the script has the correct execution permissions:
     ```bash
     chmod +x run.sh
     ```

2. **Docker Container Fails to Start:**
   - Ensure that you have the `ros:noetic-desktop-full` image locally. You can pull the image with:
     ```bash
     docker pull ros:noetic-desktop-full
     ```

3. **ROS Bag Not Being Recorded:**
   - Check the ROS launch file (`d435i.launch`) for any issues with node configuration.
   - Ensure that the necessary devices are properly connected (e.g., RealSense camera).

## Contributing

Feel free to open issues or submit pull requests if you'd like to contribute to the project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
