import os
import time
import json
from datetime import datetime
from xhand_control_left import XHandControlExample

# 设置 LD_LIBRARY_PATH 环境变量
script_dir = os.path.dirname(os.path.realpath(__file__))
xhandcontrol_library_dir = os.path.join(script_dir, "lib")
os.environ["LD_LIBRARY_PATH"] = (
    xhandcontrol_library_dir + os.pathsep + os.environ.get("LD_LIBRARY_PATH", "")
)
print(f"LD_LIBRARY_PATH: {os.environ['LD_LIBRARY_PATH']}\n")

def replay_recording(filename, xhand_exam_right):
    with open(filename, 'r') as f:
        i = 0
        for line in f:
            # i+=1
            # if i % 10:
            #     continue
            frame = json.loads(line)
            print(f"Step {frame['step']} @ {frame['time']:.3f}s")
            
            # # 获取左手数据
            # left_joints = [j['actual'] for j in frame['left']['joints']]
            # left_tactile = frame['left']['tactile']
            
            # 获取右手数据
            right_joints = [j['actual'] for j in frame['right']['joints']]
            right_tactile = frame['right']['tactile']
            
            # xhand_exam_left.realtime(left_joints)
            xhand_exam_right.realtime(right_joints)
            time.sleep(0.01)
            # 在这里添加您的复现逻辑
            # 例如：control_robot(left_joints, right_joints)

if __name__ == "__main__":
    # 通讯方式二选一，当前支持 EtherCAT 和 RS485
    # First of all, open device 
    device_identifier = {}
    # EtherCAT
    device_identifier['protocol'] = 'EtherCAT'
    xhand_exam_right = XHandControlExample()
    xhand_exam_right.exam_open_device(device_identifier)

    # Then, get hands id
    xhand_exam_right.exam_read_device_info()
    xhand_exam_right.exam_reset_sensor()
    xhand_exam_right.exam_set_hand_id(new_id=1)

    # !! Waring: This function will send command to devic
    xhand_exam_right.exam_send_command()

    time.sleep(1)

    # # RS485
    # device_identifier['protocol'] = 'RS485'
    # xhand_exam_right = XHandControlExample()
    # # Get serial port list, choose ttyUSB*
    # xhand_exam_right.exam_enumerate_devices('RS485')
    # device_identifier["serial_port"] = '/dev/ttyUSB0'
    # device_identifier['baud_rate'] = 3000000
    # xhand_exam_right.exam_open_device(device_identifier)

    # # Then, get hands id
    # xhand_exam_right.exam_read_device_info()
    # xhand_exam_right.exam_reset_sensor()
    # xhand_exam_right.exam_set_hand_id(new_id=2)
    # xhand_exam_right.exam_send_command()

    replay_recording('output/test6/data.json', xhand_exam_right)

    # !! Waring: This function will send command to devic
    xhand_exam_right.exam_send_command()