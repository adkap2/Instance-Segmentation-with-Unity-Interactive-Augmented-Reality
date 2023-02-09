import numpy as np
import urllib
import time
import cv2
from yolact_edge.inference import YOLACTEdgeInference
import zmq
import struct
import gzip

# weights = "yolact_edge_resnet50_54_800000.pth"
weights = "yolact_base_26666_1280000.pth"
# All available model configs, depends on which weights
# you use. More info could be found in data/config.py.
model_configs = [
    'yolact_base_config',
    'yolact_edge_config',
    'yolact_edge_mobilenetv2_config',
    'yolact_edge_vid_config',
    'yolact_edge_vid_minimal_config',
    'yolact_edge_vid_trainflow_config',
    'yolact_edge_youtubevis_config',
    'yolact_resnet50_config',
    'yolact_resnet152_config',
    'yolact_edge_resnet50_config',
    'yolact_edge_vid_resnet50_config',
    'yolact_edge_vid_trainflow_resnet50_config',
    'yolact_edge_youtubevis_resnet50_config',
]
config = model_configs[1]
# All available model datasets, depends on which weights
# you use. More info could be found in data/config.py.
datasets = [
    'SyntheticHome',
    'coco2014_dataset',
    'coco2017_dataset',
    'coco2017_testdev_dataset',
    'flying_chairs_dataset',
    'youtube_vis_dataset',
]
dataset = datasets[0]
# Used tensorrt calibration
calib_images = "./data/calib_images"
# Override some default configuration
config_ovr = {
    'use_fast_nms': True,  # Does not work with regular nms
    'mask_proto_debug': False
}
model_inference = YOLACTEdgeInference(
    weights, config, dataset, calib_images, config_ovr)

context = zmq.Context()
socket = context.socket(zmq.SUB)

# Subscribe to all messages
socket.connect("tcp://localhost:5555")
socket.setsockopt(zmq.SUBSCRIBE, b"")

# print("Waiting for messages...")

print('Starting up on {} port {}'.format('localhost', 5555))

print("Waiting for messages...")

payload_size = struct.calcsize("Q")

data = b""

print("Benchmarking performance...")
start = time.time()
prev_time = 0

while True:
    t1 = time.time()
    try:
        while len(data) < payload_size:
            packet = socket.recv()

            if not packet: break
            data+=packet
        
        image_data = gzip.decompress(data)

        img = np.frombuffer(image_data, dtype=np.uint8)
        img = img.reshape((480, 640, 4))
        # # Flip image
        img = cv2.flip(img, 0)
        # # Convert to RGB
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)
        # Time inference

        # t3 = time.time()
        p = model_inference.predict(img, False)
        # t4 = time.time()
        # print(f"Time taken: {t4 - t3} seconds")

        

        print(f"Average {1 / (time.time() - prev_time)} FPS")

        if p:

            cv2.imshow("Webcam", p['img'])
            cv2.waitKey(1)
        else:
            print("No prediction")

        prev_time = time.time()
        data = b""
        t2 = time.time()
        # print(f"Time taken: {t2 - t1} seconds")


    except KeyboardInterrupt:
        print("Shutting down...")
        break
