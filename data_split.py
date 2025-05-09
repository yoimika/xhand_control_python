import re
from trans import to_euler_zyx

def parse_hand_data_left(data_str):
    """
    解析手部数据字符串，提取各关节的四元数
    
    参数:
        data_str: 包含手部数据的字符串，格式如示例
        
    返回:
        dict: 包含各关节四元数的字典，键为关节名称/编号，值为四元数列表[w, x, y, z]
    """
    # 分割左右手数据（如果存在）
    before_pipe = data_str.split('|')[0].strip()
    
    # 移除括号内的内容（如角度数据）
    cleaned = re.sub(r'\(.*?\)', '', before_pipe)
    
    # 提取所有数值并转换为float
    values = list(map(float, cleaned.strip().split()))
    
    # 提取四元数部分（跳过前3个位置数据）
    quat_values = values[3:3+80]  # 假设共20个关节，每个关节4个值
    
    # 将四元数值分组
    quaternions = [to_euler_zyx(quat_values[i:i+4], 1) for i in range(0, 80, 4)]
    # quaternions = to_euler_zyx(quaternions)

    # 创建关节字典
    joints = {
        # 手掌
        'wrist': quaternions[0],
        
        # 拇指
        'thumb_1': quaternions[1],
        'thumb_2': quaternions[2],
        'thumb_3': quaternions[3],
        # 'thumb_tip': quaternions[4],
        
        # 食指
        'index_1': quaternions[4],
        'index_2': quaternions[5],
        'index_3': quaternions[6],
        'index_tip': quaternions[7],
        
        # 中指
        'middle_1': quaternions[8],
        'middle_2': quaternions[9],
        'middle_3': quaternions[10],
        'middle_tip': quaternions[11],
        
        # 无名指
        'ring_1': quaternions[12],
        'ring_2': quaternions[13],
        'ring_3': quaternions[14],
        'ring_tip': quaternions[15],
        
        # 小指
        'pinky_1': quaternions[16],
        'pinky_2': quaternions[17],
        'pinky_3': quaternions[18],
        'pinky_tip': quaternions[19]
    }
    
    return joints

def parse_hand_data_right(data_str):
    """
    解析手部数据字符串，提取各关节的四元数
    
    参数:
        data_str: 包含手部数据的字符串，格式如示例
        
    返回:
        dict: 包含各关节四元数的字典，键为关节名称/编号，值为四元数列表[w, x, y, z]
    """
    # 分割左右手数据（如果存在）
    before_pipe = data_str.split('|')[1].strip()
    
    # 移除括号内的内容（如角度数据）
    cleaned = re.sub(r'\(.*?\)', '', before_pipe)
    
    # 提取所有数值并转换为float
    values = list(map(float, cleaned.strip().split()))

    # 提取四元数部分（跳过前3个位置数据）
    quat_values = values[3:3+80]  # 假设共20个关节，每个关节4个值
    
    # 将四元数值分组
    quaternions = [to_euler_zyx(quat_values[i:i+4], -1) for i in range(0, 80, 4)]
    # quaternions = to_euler_zyx(quaternions)

    # 创建关节字典
    joints = {
        # 手掌
        'wrist': quaternions[0],
        
        # 拇指
        'thumb_1': quaternions[1],
        'thumb_2': quaternions[2],
        'thumb_3': quaternions[3],
        # 'thumb_tip': quaternions[4],
        
        # 食指
        'index_1': quaternions[4],
        'index_2': quaternions[5],
        'index_3': quaternions[6],
        'index_tip': quaternions[7],
        
        # 中指
        'middle_1': quaternions[8],
        'middle_2': quaternions[9],
        'middle_3': quaternions[10],
        'middle_tip': quaternions[11],
        
        # 无名指
        'ring_1': quaternions[12],
        'ring_2': quaternions[13],
        'ring_3': quaternions[14],
        'ring_tip': quaternions[15],
        
        # 小指
        'pinky_1': quaternions[16],
        'pinky_2': quaternions[17],
        'pinky_3': quaternions[18],
        'pinky_tip': quaternions[19]
    }
    
    return joints

def get_data_left(joints):
    res = []
    ratio1 = 1.2
    ratio2 = 1.5
    res.append(joints['thumb_1'][2] * ratio1 - 0.2)
    res.append(joints['thumb_2'][0] * ratio1)
    res.append(joints['thumb_3'][0] * ratio1)
    res.append(joints['index_2'][1] * ratio1)
    res.append(joints['index_2'][0] * ratio2)
    res.append(joints['index_3'][0] * ratio2)
    res.append(joints['middle_2'][0] * ratio1)
    res.append(joints['middle_3'][0] * ratio1)
    res.append(joints['ring_2'][0] * ratio1)
    res.append(joints['ring_3'][0] * ratio1)
    res.append(joints['pinky_2'][0] * ratio2)
    res.append(joints['pinky_3'][0] * ratio2)
    return res

def get_data_right(joints):
    res = []
    ratio1 = 1.2
    ratio2 = 1.5
    res.append(-joints['thumb_1'][2] * ratio2 - 1.0)
    # print(res[0])
    res.append(joints['thumb_2'][0] * ratio1)
    res.append(joints['thumb_3'][0] * ratio1)
    res.append(joints['index_2'][1] * ratio1)
    res.append(joints['index_2'][0] * ratio2)
    res.append(joints['index_3'][0] * ratio2)
    res.append(joints['middle_2'][0] * ratio1)
    res.append(joints['middle_3'][0] * ratio1)
    res.append(joints['ring_2'][0] * ratio1)
    res.append(joints['ring_3'][0] * ratio1)
    res.append(joints['pinky_2'][0] * ratio2)
    res.append(joints['pinky_3'][0] * ratio2)
    return res

# # 使用示例
# data_str = "0.009999 0.000000 0.137318 0.188382 0.499764 -0.299097 -0.790752 -0.487952 -0.217172 0.170218 -0.828109 0.000000 0.000000 0.311134 0.950366 0.000000 0.000000 0.066317 0.997799 0.000000 0.000000 0.000000 1.000000 -0.010054 -0.130139 -0.076370 -0.988499 0.000000 0.000000 0.063044 0.998011 0.000000 0.000000 0.044146 0.999025 0.000000 0.000000 0.000000 1.000000 0.000000 0.000000 0.148064 0.988978 0.000000 0.000000 0.148064 0.988978 0.000000 0.000000 -0.098813 -0.995106 0.000000 0.000000 0.000000 1.000000 -0.009299 -0.086658 0.106290 0.990508 0.000000 0.000000 0.106696 0.994292 0.000000 0.000000 0.071135 0.997467 0.000000 0.000000 0.000000 1.000000 0.008819 -0.173424 -0.050017 0.983537 0.000000 0.000000 0.000000 1.000000 0.000000 0.000000 0.000000 1.000000 (0.000000 0.000000 0.000000 0.000000 0.000000) | -0.009999 0.000000 0.137318 -0.216117 0.464132 -0.286854 0.809685 0.429610 -0.201048 0.199200 0.857517 0.000000 0.000000 -0.284236 0.958755 0.000000 0.000000 -0.029813 0.999556 0.000000 0.000000 0.000000 1.000000 0.005561 -0.130408 -0.042242 0.990545 0.000000 0.000000 -0.034863 0.999392 0.000000 0.000000 -0.024407 0.999702 0.000000 0.000000 0.000000 1.000000 0.000000 0.000000 -0.107179 0.994240 0.000000 0.000000 -0.107179 0.994240 0.000000 0.000000 -0.071457 0.997444 0.000000 0.000000 0.000000 1.000000 -0.011469 0.086398 -0.131087 0.987533 0.000000 0.000000 -0.131587 0.991305 0.000000 0.000000 -0.087779 0.996140 0.000000 0.000000 0.000000 1.000000 -0.006368 0.173531 -0.036117 0.984145 0.000000 0.000000 -0.054996 0.998487 0.000000 0.000000 -0.036638 0.999329 (0.000000 0.000000 0.000000 0.000000 0.000000)"

# joint_data = parse_hand_data_left(data_str)

# # 打印前3个关节的四元数
# for joint_name in joint_data:
#     print(f"{joint_name}: {joint_data[joint_name]}")