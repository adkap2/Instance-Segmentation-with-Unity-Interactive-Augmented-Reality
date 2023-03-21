# Imports

import numpy as np
import urllib
import time
import cv2
from yolact_edge.inference import YOLACTEdgeInference
import zmq
import struct
import gzip

# Load Model

# weights = "yolact_edge/weights/yolact_base_54_800000.pth"
weights = "weights/yolact_edge_54_800000.pth"
# weights = "weights/yolact_base_26666_1280000.pth"
# weights = "yolact_edge/weights/synthetic_home_20456_900084_interrupt.pth"
# weights = "weights/yolact_base_20454_900000.pth"
# All available model configs, depends on which weights
# Load YOLACT Configuration

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

# Load dataset
datasets = [
    'SyntheticHome',
    'coco2014_dataset',
    'coco2017_dataset',
    'ConcatDataset',
    'coco2017_testdev_dataset',
    'flying_chairs_dataset',
    'youtube_vis_dataset',
]
dataset = datasets[2]
# Used tensorrt calibration
calib_images = "./data/calib_images"
# Override some default configuration
config_ovr = {
    '--fast_nms': True,  # Does not work with regular nms
    'mask_proto_debug': False,
   #  '--use_tensorrt_safe_mode': True,
}
# !export CUDA_MODULE_LOADING=LAZY
# Enable lazy loading


# Load Model
model_inference = YOLACTEdgeInference(
    weights, config, dataset, calib_images, config_ovr)

# Total time to load = 3m 30s

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

            if not packet:
                break
            data += packet
        
        image_data = gzip.decompress(data)

        img = np.frombuffer(image_data, dtype=np.uint8)

        img = img.reshape((480, 640, 4))
        img = cv2.resize(img, (1280, 960))

        # Flip image
        img = cv2.flip(img, 0)
        # Convert to RGB
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)

        # img = cv2.convertScaleAbs(img, alpha=3.5, beta=5)

        # Time inference
        p = model_inference.predict(img, False)

        print(f"Average {1 / (time.time() - prev_time)} FPS")

        if p:
            cv2.imshow("Unity Cam", p['img'])
            # cv2.resizeWindow("Garnet Cam", 1280, 960)
            # Change window size
            cv2.waitKey(1)
        else:
            print("No prediction")

        prev_time = time.time()
        data = b""
        t2 = time.time()

    except KeyboardInterrupt:
        print("Shutting down...")
        break
# close the socket
socket.close()