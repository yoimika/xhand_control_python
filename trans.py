import math
import numpy as np

def to_euler_zyx(t, dir, degrees=False):
    """
    将四元数转换为ZYX顺序的欧拉角（yaw-pitch-roll）
    参数：
        w, x, y, z: 四元数分量（需已归一化）
        degrees: 返回角度制（默认True）
    返回：
        (yaw, pitch, roll) 单位：度（默认）或弧度
    """
    x = t[0]
    y = t[1]
    z = t[2]
    w = t[3]
    # 归一化四元数
    norm = math.sqrt(w**2 + x**2 + y**2 + z**2)
    w /= norm
    x /= norm
    y /= norm
    z /= norm

    # 计算旋转矩阵元素
    m00 = 1 - 2*y*y - 2*z*z
    m01 = 2*x*y - 2*z*w
    m02 = 2*x*z + 2*y*w
    
    m10 = 2*x*y + 2*z*w
    m11 = 1 - 2*x*x - 2*z*z
    m12 = 2*y*z - 2*x*w
    
    m20 = 2*x*z - 2*y*w
    m21 = 2*y*z + 2*x*w
    m22 = 1 - 2*x*x - 2*y*y

    # 提取欧拉角（ZYX顺序）
    pitch = dir * math.asin(m02)
    roll = -dir * math.atan2(m12, m22)
    yaw = -dir * math.atan2(m01, m00)

    if degrees:
        return (
            math.degrees(yaw),
            math.degrees(pitch),
            math.degrees(roll)
        )
    else:
        return (yaw, pitch, roll)