import shutil
import subprocess
import imageio
import numpy as np


def path(string):
    return string


def add_white_side(input_image_path):
    # 图片添加白边
    temp_output_path = input_image_path + "_temp.png"  # 临时输出文件
    try:
        command_parts = [
            "ffmpeg",
            "-i",
            input_image_path,
            "-vf",
            "pad=width=ceil(iw*1.5):height=ceil(ih*1.5):x=(ceil(iw*0.25)):y=(ceil(ih*0.25)):color=white",
            "-y",
            temp_output_path  # 输出到临时文件
        ]
        subprocess.run(command_parts, check=True)
        print(f'图片添加白边成功: {input_image_path}')
        shutil.move(temp_output_path, input_image_path)  # 用临时文件覆盖原文件
        return input_image_path
    except Exception as e:
        print(f"图片添加白边失败: {e}")
        return input_image_path


def rreplace(s, old, new, occurrence):
    li = s.rsplit(old, occurrence)
    return new.join(li)
