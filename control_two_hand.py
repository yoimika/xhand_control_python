import os
import time
import socket
from xhand_control_example import XHandControlExample
from data_split import parse_hand_data_left, parse_hand_data_right, get_data_left, get_data_right
from double_buffer_client import DoubleBufferClient

# 设置 LD_LIBRARY_PATH 环境变量
# script_dir = os.path.dirname(os.path.realpath(__file__))
# xhandcontrol_library_dir = os.path.join(script_dir, "lib")
# os.environ["LD_LIBRARY_PATH"] = (
#     xhandcontrol_library_dir + os.pathsep + os.environ.get("LD_LIBRARY_PATH", "")
# )
# print(f"LD_LIBRARY_PATH: {os.environ['LD_LIBRARY_PATH']}\n")

# data_queue0 = Queue(maxsize=100)
# data_queue1 = Queue(maxsize=100)

def start_server(xhand_exam_left: XHandControlExample, xhand_exam_right: XHandControlExample, host='0.0.0.0', port=54321):  # 改为0.0.0.0监听所有接口
    socket_manager = DoubleBufferClient(host=host, port=port)
    socket_manager.listen()
    while True:
        # data = socket_manager.rec()
        data = socket_manager.get_data()
        data_left = parse_hand_data_left(data)
        data_right = parse_hand_data_right(data)
        
        # for joint_name in data:
        #     print(f"{joint_name}: {data[joint_name]}")
        data_left = get_data_left(data_left)
        xhand_exam_left.realtime(data_left)
        data_right = get_data_right(data_right)
        xhand_exam_right.realtime(data_right)


if __name__ == "__main__":
    device_identifier = {}

    # left hand
    device_identifier['protocol'] = 'RS485'
    xhand_exam_left = XHandControlExample()
    xhand_exam_left.exam_enumerate_devices('RS485')
    device_identifier["serial_port"] = '/dev/ttyUSB2'
    device_identifier['baud_rate'] = 3000000
    xhand_exam_left.exam_open_device(device_identifier)

    # Then, get hands id
    xhand_exam_left.exam_read_device_info()
    xhand_exam_left.exam_reset_sensor()
    xhand_exam_left.exam_set_hand_id(new_id=1)

    # !! Waring: This function will send command to devic
    xhand_exam_left.exam_send_command()

    # right hand
    device_identifier['protocol'] = 'RS485'
    xhand_exam_right = XHandControlExample()
    xhand_exam_right.exam_enumerate_devices('RS485')
    device_identifier["serial_port"] = '/dev/ttyUSB3'
    device_identifier['baud_rate'] = 3000000
    xhand_exam_right.exam_open_device(device_identifier)

    # Then, get hands id
    xhand_exam_right.exam_read_device_info()
    xhand_exam_right.exam_reset_sensor()
    xhand_exam_right.exam_set_hand_id(new_id=2)

    # !! Waring: This function will send command to devic
    xhand_exam_right.exam_send_command()

    start_server(xhand_exam_left, xhand_exam_right)

    # Close device (important)
    xhand_exam_left.set_hand_mode(mode=0)
    xhand_exam_left.exam_close_device()

    xhand_exam_right.set_hand_mode(mode=0)
    xhand_exam_right.exam_close_device()
    