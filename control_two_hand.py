import os
import time
import socket
from xhand_control_left import XHandControlExample
from data_split import parse_hand_data_left, parse_hand_data_right, get_data_left, get_data_right, get_latest_data
from camera import *
from write import DataRecorder
# from multiprocessing import Process, Queue
from queue import Queue
# from tmp import Socket
from double_buffer_client import DoubleBufferClient

# 设置 LD_LIBRARY_PATH 环境变量
script_dir = os.path.dirname(os.path.realpath(__file__))
xhandcontrol_library_dir = os.path.join(script_dir, "lib")
os.environ["LD_LIBRARY_PATH"] = (
    xhandcontrol_library_dir + os.pathsep + os.environ.get("LD_LIBRARY_PATH", "")
)
print(f"LD_LIBRARY_PATH: {os.environ['LD_LIBRARY_PATH']}\n")

# data_queue0 = Queue(maxsize=100)
# data_queue1 = Queue(maxsize=100)

def start_server(xhand_exam_left, xhand_exam_right, recorder, rs_pipelines, host='127.0.0.1', port=54321):  # 改为0.0.0.0监听所有接口
    
    socket_manager = DoubleBufferClient(host=host, port=port)
    socket_manager.listen()
    # socket_manager.init()
    while True:
        data = socket_manager.get_data()
        data_left = parse_hand_data_left(data)
        # for joint_name in data:
        #     print(f"{joint_name}: {data[joint_name]}")
        data_left = get_data_left(data_left)
        xhand_exam_left.realtime(data_left)

        data_right = parse_hand_data_right(data)
        data_right = get_data_right(data_right)
        xhand_exam_right.realtime(data_right)



    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen(5)
        print(f"服务器已启动，监听 {host}:{port} (外部可访问)")
        
        hhhhhh = 0
        print(f"服务器已启动，监听 {host}:{port} (按 Ctrl+C 退出)")
        
        queue = Queue(maxsize=1024)

        try:
            while True:
                conn, addr = s.accept()
                with conn:
                    # print(f"接收到来自 {addr} 的连接")
                    t1 = time.time()
                    data = conn.recv(4096)
                    # print(f"接收到数据: {data.decode('ASCII')}")
                    # conn.sendall(b"Message received")

                    # trans to what I need
                    data = data.decode('ASCII')
                    # print(data)
                    # print(len(data))
                    if len(data) > 700:
                        # print()
                        data = get_latest_data(data)
                        # print('left hand')
                        data_left = parse_hand_data_left(data)
                        # for joint_name in data_left:
                        #     print(f"{joint_name}: {data_left[joint_name]}")
                        data_left = get_data_left(data_left)
                        xhand_exam_left.realtime(data_left)

                        # print()
                        # print('right_hand')
                        data_right = parse_hand_data_right(data)
                        # for joint_name in data_right:
                        #     print(f"{joint_name}: {data_right[joint_name]}")
                        data_right = get_data_right(data_right)
                        xhand_exam_right.realtime(data_right)

                        # record right hand data
                        left_state = xhand_exam_left.get_current_state()
                        right_state = 1
                        # right_state = xhand_exam_right.get_current_state()
                        hhhhhh+=1
                        # t1 = time.time()
                        if left_state and hhhhhh % 10 == 0:
                            tframe=recorder.record_frame(left_state, right_state)
                            # pcd0, pcd_color0, depth_img0, color_img0 = rs_pipelines[0].get_all_data()
                            # queue.put(1)
                            # pcd1, pcd_color1, depth_img1, color_img1 = rs_pipelines[1].get_all_data()
                            # if not data_queue0.full():
                            #     data_queue0.put((color_img0, tframe))
                            # else:
                            #     print("queue0 is full")
                            # if not data_queue1.full():
                            #     data_queue1.put((color_img1, tframe))
                            # else:
                            #     print("queue1 is full")
                        
                    print('ccccccccccc', (time.time() - t1) * 1000)
        except KeyboardInterrupt:
            running = False
            print("\n接收到退出信号，关闭服务器...")
        finally:
            s.close()  # 显式关闭（虽然 with 语句会自动关闭，但显式调用更清晰）

def save_data_process(data_queue, ind, dirs):
    while True:
        try:
            image, frame = data_queue.get(0.5)
            color_path = f'{dirs}/images/color_{ind}_{frame}.jpg'
            cv2.imwrite(color_path, color_img, [cv2.IMWRITE_JPEG_QUALITY, 50])
            print(f'{ind}  aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
        except data_queue.Empty:
            continue

if __name__ == "__main__":

    # setup camera
    oldmask = os.umask(000)
    serials, ctx = find_devices()
    
        # 通讯方式二选一，当前支持 EtherCAT 和 RS485
    # First of all, open device 
    device_identifier = {}

    # # RS485
    # device_identifier['protocol'] = 'RS485'
    # xhand_exam_left = XHandControlExample()
    # # Get serial port list, choose ttyUSB*
    # xhand_exam_left.exam_enumerate_devices('RS485')
    # device_identifier["serial_port"] = '/dev/ttyUSB0'
    # device_identifier['baud_rate'] = 3000000
    # xhand_exam_left.exam_open_device(device_identifier)

    # EtherCAT
    device_identifier['protocol'] = 'EtherCAT'
    xhand_exam_left = XHandControlExample()
    xhand_exam_left.exam_open_device(device_identifier)

    # Then, get hands id
    xhand_exam_left.exam_read_device_info()
    xhand_exam_left.exam_reset_sensor()
    xhand_exam_left.exam_set_hand_id(new_id=1)

    # !! Waring: This function will send command to devic
    xhand_exam_left.exam_send_command()


    # RS485
    device_identifier['protocol'] = 'RS485'
    xhand_exam_right = XHandControlExample()
    # Get serial port list, choose ttyUSB*
    xhand_exam_right.exam_enumerate_devices('RS485')
    device_identifier["serial_port"] = '/dev/ttyUSB0'
    device_identifier['baud_rate'] = 3000000
    xhand_exam_right.exam_open_device(device_identifier)

    # # EtherCAT
    # device_identifier['protocol'] = 'EtherCAT'
    # xhand_exam_right = XHandControlExample()
    # xhand_exam_right.exam_open_device(device_identifier)


    # Then, get hands id
    xhand_exam_right.exam_read_device_info()
    xhand_exam_right.exam_reset_sensor()
    xhand_exam_right.exam_set_hand_id(new_id=2)

    # !! Waring: This function will send command to devic
    xhand_exam_right.exam_send_command()

    # rs_pipelines=1
    # 初始化数据记录器
    base_name = input("请输入记录文件名（留空使用时间戳）: ").strip() or None
    # time_recorder = time.time()
    # print(time_recorder)
    recorder = DataRecorder(base_name)
    rs_pipelines = [RealSenseD405(device=ser, resolution='mid') for ser in serials]
    #t1=time.time()

    
    # p0 = Process(target=save_data_process, args=(data_queue0, 0, base_name, ))
    # p0.start
    # p1 = Process(target=save_data_process, args=(data_queue1, 1, base_name, ))
    # p1.start

    start_server(xhand_exam_left, xhand_exam_right, recorder, rs_pipelines)

    # Close device (important)
    xhand_exam_left.set_hand_mode(mode=0)
    xhand_exam_left.exam_close_device()

    xhand_exam_right.set_hand_mode(mode=0)
    xhand_exam_right.exam_close_device()
    