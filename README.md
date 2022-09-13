# CMPE-295
Interactive Augmented Reality for Semantic Segmentation on Indoor Environments

    install unity
    Client server communication python -> unity (TCPIP?)
    Python (hello world) displayed under unity
    Unity create simple 3D object such as a cube
    Use python to move the cube up then down, left then right
    Have image from python sent to unity and display image: 
    Perform on virtual screen in unity
    Send video to virtual display screen directly from camera such as youtube or webcam
    Later do a video from file or webcam
    Establish readme for each task


1. Install Unity

<img src="images/Screen Shot 2022-08-30 at 10.45.50 AM.png" alt = "image" width ="400"/>


2. Python hello world displayed under unity

<img src="images/Screen Shot 2022-08-30 at 10.41.07 AM.png" alt = "image" width ="400"/>
<img src="images/Screen%20Shot%202022-08-30%20at%2010.41.14%20AM.png" alt="image", width ="800"/>


3. Unity create 3D object such as a cube and use python to move the cube up then down, left then right

- Modified code from [here](https://github.com/CanYouCatchMe01/CSharp-and-Python-continuous-communication)
  to move the cube up and down, left and right
   
<img src= "videos/unity_cube_move.gif" alt = "gif" width = "400"/>



## Unity ML Tutorial

1. Install Unity Kart Racing [here](https://learn.unity.com/project/karting-template)
2. Complete the In-editor Tutorials
3. Follow Kart ML Agent Tutorial [here](https://www.youtube.com/watch?v=gYwWolRFt98)
   - Kart Classic Training Demo Scene
   - Train agent to achieve a goal such as driving without colliding with the track walls
   - Academy collects all observations done by the agents and trains the agents
   - Kart ML Agent behaivor parameters allows us to define how the agent interacts
 - <img src = "images/Kart_ML_Track.png" alt = "Kart ML" width = "300"/>
- Connect Install Python-Unity-ML Dependencies inside of the unity project directory  with the following command 
  - `pip install -Iv mlagents==0.13.0`
- Create new Kart Academy prefab
- create Training environment Game object
-  To run training run:
   -  ` mlagents-learn Assets/Karting/Prefabs/AI/kart_mg_trainer_config.yaml --train --run-id=custom-track-1`
   -  Yielded compatibility error between unity and mlagents in python:
"Traceback (most recent call last):
  File "/Users/adam/opt/anaconda3/lib/python3.7/multiprocessing/process.py", line 297, in _bootstrap
    self.run()
  File "/Users/adam/opt/anaconda3/lib/python3.7/multiprocessing/process.py", line 99, in run
    self._target(*self._args, **self._kwargs)
  File "/Users/adam/Desktop/SJSU/CMPE295A/CMPE-295/Unity_Tutorial/Unity Karting MicroGame Tutorial/venv/lib/python3.7/site-packages/mlagents/trainers/subprocess_env_manager.py", line 100, in worker
    worker_id, [shared_float_properties, engine_configuration_channel]
  File "/Users/adam/Desktop/SJSU/CMPE295A/CMPE-295/Unity_Tutorial/Unity Karting MicroGame Tutorial/venv/lib/python3.7/site-packages/mlagents/trainers/learn.py", line 425, in create_unity_environment
    side_channels=side_channels,
  File "/Users/adam/Desktop/SJSU/CMPE295A/CMPE-295/Unity_Tutorial/Unity Karting MicroGame Tutorial/venv/lib/python3.7/site-packages/mlagents_envs/environment.py", line 135, in __init__
    f"The API number is not compatible between Unity and python. "

    