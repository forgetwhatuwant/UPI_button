from gpiozero import Button
import time
import sys
import os
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')

if os.path.exists(libdir):
    sys.path.append(libdir)
from datetime import datetime  # 用于获取当前时间
from PIL import Image, ImageDraw, ImageFont
from waveshare_epd import epd2in13_V4
import subprocess  # 用于运行shell脚本
from pressing_log import handle_long_press, handle_short_press

# 初始化 gpiozero 按钮
button = Button(15, pull_up=True)

# 初始化e-Paper
epd = epd2in13_V4.EPD()
epd.init()
epd.Clear(0xFF)  # 清空屏幕

# 加载自定义字体并设置字体大小
font_path = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
font_size = 24  # 设置为较大的字体大小
font = ImageFont.truetype(font_path, font_size)

def display_on_epaper(text, update_time=False):
    image = Image.new('1', (epd.height, epd.width), 255)  # 创建一个白色背景的图像
    draw = ImageDraw.Draw(image)
    
    # 显示系统状态文本，使用大字体
    draw.text((10, 10), text, font=font, fill=0)

    if update_time:
        # 显示时间在右下角
        current_time = datetime.now().strftime("%H:%M:%S")
        
        # 获取文本边界框的大小
        bbox = draw.textbbox((0, 0), current_time, font=font)
        time_width = bbox[2] - bbox[0]
        time_height = bbox[3] - bbox[1]

        draw.text((epd.height - time_width - 10, epd.width - time_height - 10), current_time, font=font, fill=0)

    epd.displayPartial(epd.getbuffer(image))

# 初始化系统状态
system_states = ["Docker shutdown", "Docker OK", "ROS Run", "ROS Idle"]
system_state = system_states[0]
display_on_epaper("Docker shutdown", update_time=True)

pressed_time = None  # 初始化按钮按下时间
long_press_duration = 3  # 长按3秒
rosbag_recording = False  # rosbag录制状态
docker_started = False  # Docker是否已启动roslaunch
container_id = None  # 初始化容器 ID 变量


# 主循环
while True:
    if button.is_pressed:
        if pressed_time is None:
            pressed_time = time.time()
    else:
        if pressed_time is not None:
            press_duration = time.time() - pressed_time
            if press_duration < long_press_duration:
                handle_short_press()
            else:
                handle_long_press()
            pressed_time = None

    time.sleep(0.1)
