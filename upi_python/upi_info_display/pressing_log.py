import subprocess  # 用于运行shell脚本
import sys
import os



# 初始化系统状态
system_states = ["Docker shutdown", "Docker OK", "ROS Run", "ROS Idle"]
system_state = system_states[0]


pressed_time = None  # 初始化按钮按下时间
long_press_duration = 3  # 长按3秒
rosbag_recording = False  # rosbag录制状态
docker_started = False  # Docker是否已启动roslaunch
container_id = None  # 初始化容器 ID 变量

def handle_long_press():
    global docker_started, system_state, container_id
    if not docker_started:
        print("Long press detected. Running roslaunch in Docker")
        # 使用 os.path.expanduser 展开 ~ 为完整路径
        script_path = os.path.expanduser("~/upi_python/upi_info_display/run.sh")
        
        result = subprocess.run([script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

# 获取 run.sh 输出的容器 ID
        if result.returncode == 0:  # 确保脚本成功执行
            container_id = result.stdout.strip()  # 去除多余空格和换行符
        if container_id:
              print(f"Container ID: {container_id}")
        else:
              print("No container ID returned.")

        
        # 停止 rosbag 记录
        try:
            if container_id:  # 确保容器 ID 存在
                subprocess.run(["docker", "exec", container_id, "pkill", "rosbag"])
                print("rosbag recording stopped.")
        except Exception as e:
            print(f"Error stopping rosbag recording: {e}")
        
        # 停止 Docker 容器
        try:
            if container_id:
                subprocess.run(["docker", "stop", container_id])
                print("Docker container stopped.")
                docker_started = False  # 更新状态
                system_state = system_states[0]  # 显示 Docker 已停止
                display_on_epaper(system_state, update_time=True)
        except Exception as e:
            print(f"Error stopping Docker container: {e}")


def handle_short_press():
    global rosbag_recording, system_state, container_id
    if docker_started and container_id:  # 确保 Docker 已启动并且容器 ID 存在
        if not rosbag_recording:
            print("Starting rosbag recording")
            # 运行 rosbag 录制
            subprocess.Popen(["docker", "exec", container_id, "rosbag", "record", "-a"])
            system_state = system_states[2]  # 设置为 Recording
            rosbag_recording = True
        else:
            print("Stopping rosbag recording")
            # 停止 rosbag 录制
            subprocess.Popen(["docker", "exec", container_id, "pkill", "rosbag"])
            system_state = system_states[3]  # 设置为 Stopped
            rosbag_recording = False
        display_on_epaper(system_state, update_time=True)
    else:
        print("Docker container is not running or container_id is not available.")
        display_on_epaper("Error: Docker not running", update_time=True)

