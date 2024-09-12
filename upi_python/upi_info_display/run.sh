#!/bin/bash

# 定义一个文件来存储容器 ID
CID_FILE="/tmp/docker_cid.txt"

# 启动 Docker 容器，并执行 roslaunch 启动 RealSense 相机节点
docker container run -it --rm --privileged --net=host \
    --volume=/dev:/dev \
    --volume="/home/${USER}/codes":"/home/codes":rw  \
    --cidfile="$CID_FILE" \
    ros:noetic-desktop-full \
    bash -c "
        roslaunch /home/codes/d435i.launch &
        rosbag record -a --output-name=my_rosbag.bag
    "

# 输出容器 ID
if [ -f "$CID_FILE" ]; then
    cat "$CID_FILE"  # 输出容器ID到标准输出
    rm -f "$CID_FILE"  # 删除保存容器ID的临时文件
else
    echo "Failed to retrieve Docker container ID."
fi
