import os
import time
import json
from datetime import datetime
from xhand_control_left import XHandControlExample
from camera import *
from multiprocessing import Process, Queue
# import concurrent.futures
#import asyncio
from concurrent.futures import ThreadPoolExecutor

# 设置 LD_LIBRARY_PATH 环境变量
script_dir = os.path.dirname(os.path.realpath(__file__))
xhandcontrol_library_dir = os.path.join(script_dir, "lib")
os.environ["LD_LIBRARY_PATH"] = (
    xhandcontrol_library_dir + os.pathsep + os.environ.get("LD_LIBRARY_PATH", "")
)
print(f"LD_LIBRARY_PATH: {os.environ['LD_LIBRARY_PATH']}\n")


def save_camera_image(self, pipeline, ind, dirs, frame):
    """类内方法版（可选，方便访问类属性）"""
    pcd, pcd_color, depth_img, color_img = pipeline.get_all_data()
    color_path = os.path.join(dirs, f"images/color_{ind}_{frame}.jpg")
    cv2.imwrite(color_path, color_img, [cv2.IMWRITE_JPEG_QUALITY, 50])
    print(f"相机{ind}保存完成: {color_path}")


class DataRecorder:
    def __init__(self, base_filename):
        self.start_time = time.time()
        self.step_count = 0
        self.base_filename = base_filename or datetime.now().strftime("%Y%m%d_%H%M%S")
        self.file_handle = None
        self._prepare_file()
        self.dirs
    
    def _prepare_file(self):
        output = 'output'
        dirs = f"{output}/{self.base_filename}"
        counter = 0
        while os.path.exists(dirs):
            counter += 1
            dirs = f"{output}/{self.base_filename}_{counter}" 
        os.makedirs(dirs, mode=0o777, exist_ok=True)
        os.makedirs(f"{dirs}/images", mode=0o777, exist_ok=True)
        self.dirs = dirs

        filename = f"{dirs}/data.json"
        
        self.file_handle = open(filename, 'w')
        print(f"Logging to: {filename}")

    def record_frame(self, left_data, right_data):
        frame = {
            "step": self.step_count,
            "time": time.time() - self.start_time,
            "left": left_data,
            # "right": right_data
        }
        self.file_handle.write(json.dumps(frame) + '\n')
        self.file_handle.flush()
        
        # p = Process(target=camerapicture, args=(rs_pipelines, self.dirs, self.step_count))
        # p.start()  # 异步执行，主程序不等待
        
        # t1 = time.time()
        # # camerapicture(rs_pipelines, self.dirs, self.step_count)

        # t2 = time.time()
        # print('aaaaaaaaaaa', (t2 - t1) * 1000)
        self.step_count += 1
        # print("now step", self.step_count)
        return self.step_count - 1

    # def record_frame(self, left_data, right_data):
    #     frame = {
    #         "step": self.step_count,
    #         "time": time.time() - self.start_time,
    #         "left": left_data,
    #         "right": right_data
    #     }
    #     self.file_handle.write(json.dumps(frame) + '\n')
    #     self.file_handle.flush()
    #     self.step_count += 1

    def close(self):
        if self.file_handle:
            self.file_handle.close()

async def main():
    pass

count=1
if __name__ == "__main__":
    oldmask = os.umask(000)
    serials, ctx = find_devices()
    rs_pipelines = [RealSenseD405(device=ser, resolution='mid') for ser in serials]
    # rs_pipelines=1
    # 初始化数据记录器
    base_name = input("请输入记录文件名（留空使用时间戳）: ").strip() or None
    recorder = DataRecorder(base_name)
    if count==1:
        t1=time.time()
        count=2
    
    
    
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
    # xhand_exam_right.exam_set_hand_id(new_id=0)

    # xhand_exam_right.exam_send_command()

    xhand_exam_right.set_hand_mode(mode=0)
    # xhand_exam_left.set_hand_mode(mode=0)
    
    while True:

        # 记录当前状态
        # left_state = xhand_exam_left.get_current_state()
        right_state = xhand_exam_right.get_current_state()
        # xhand_exam_right.exam_read_state()
        if right_state:
            recorder.record_frame(right_state, rs_pipelines)
        # if left_state and right_state:
        #     recorder.record_frame(left_state, right_state)
        time.sleep(0.01)
        #cv2.imshow("Color Stream", color_img)
        if cv2.waitKey(1) == 27:  # ESC退出
            print(f"t1:{t1}")
            break


    # !! Waring: This function will send command to devic
    os.umask(oldmask)
    xhand_exam_right.exam_send_command()