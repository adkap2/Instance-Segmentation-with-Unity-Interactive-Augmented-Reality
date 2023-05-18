# Github Source Link: https://github.com/Unity-Technologies/SyntheticHomes
https://github.com/Unity-Technologies/com.unity.perception

# Website: https://unity.com/products/computer-vision#unity-perception-10

# Introduction
The Synthetic Homes generator is a tool provided by Unity, a popular game engine, that enables the creation of synthetic 3D environments, including indoor home settings. These environments can be customized to simulate various scenarios, and objects can be placed and arranged to simulate a variety of real-life situations. The Synthetic Homes generator also automatically generates accurate annotations for each object in the scene, which can be used for training and evaluation purposes.

Synthetic Homes can be utilized in real-time instance segmentation tasks as a source of training data. By generating synthetic data using Synthetic Homes, a large and diverse dataset can be created, which can be used to train instance segmentation models to detect and segment objects in various indoor home environments. This synthetic data can be used to augment real-world data, leading to more robust and accurate models. Additionally, since the data is synthetic, the annotation process can be automated, allowing for a more efficient data preparation pipeline. Overall, the use of Synthetic Homes can significantly aid in the development of real-time instance segmentation models for indoor home environments.

The Synthetic Homes application is derived from the Unity Perception package. This package provides a range of tools for generating randomized synthetic computer vision datasets with ground-truth annotations. The Synthetic Homes generator is one such tool provided by the Unity Perception package, which enables the creation of synthetic 3D indoor home environments for training and evaluation purposes in computer vision applications such as real-time instance segmentation.

The dataset generated from this application is in the SOLO format. It must be converted to the COCO format prior to model training and evaluation. 

# Installation


Note: This application was executed using Windows 10 and DX12 with DXR compatible GPU for path tracing (list available here: https://docs.unity3d.com/Packages/com.unity.render-pipelines.high-definition@14.0/manual/Ray-Tracing-Getting-Started.html)
The application will fall back to rasterization if DXR capable hardware is not detected.

Clone the repository: Git clone https://github.com/Unity-Technologies/SyntheticHomes.git

Download the executable:
From here  https://github.com/Unity-Technologies/SyntheticHomes/releases download all the files. 
- Place all files in the same directory 
- Extract them to get a tar file again 
- Extract that to get the folder containing the SyntheticHomes.exe file and place that executable file inside the above cloned repository.

# Modifying the configuration file

1. Open the “SampleScenarioConfiguration.json” file which is inside the repository directory
2. Inside the list of sensors, set all labelers to false except “instancesegmentationlabeler”
3. Within randomizers, one can enable or disable each element to modify the executed scene

# Running the Executable
1. Open a command prompt and navigate to the executable location
2. Run the application: start SyntheticHomes.exe config-file=SampleScenarioConfiguration.json --resolution=640x480 --output-path D:\SyntheticHomes\data
3. View each generated image during runtime

# Citation
[1]
Unity Technologies, "Unity SynthHomes: A Synthetic Home Interior Dataset Generator," 2022. [Online]. Available: https://github.com/Unity-Technologies/SynthHomes. [Accessed: Mar. 02, 2023].








