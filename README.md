# CMPE-295
Interactive Augmented Reality for Semantic Segmentation on Indoor Environments

Python Hello-The-World to Unity:


Follow the steps mentioned in this document to install Python for Unity: https://docs.unity3d.com/Packages/com.unity.scripting.python@2.0/manual/installation.html

Launch Unity Hub to create a new unity project (one can use 2D template for project) to print Hello-The-World in python Editor inside Unity.

Go to the folder in your computer where the unity project is saved and under “Packages” folder edit “manifest.json” file. Add “com.unity.scripting.python”: “2.0.1-preview.2” as the first argument of dependencies() in manifest.json file.

Now go to unity and launch the project. Click on Edit -> Project Settings -> Python for        Unity, in Python Process Versions add the path of the python.exe executable file which is under the folder “Python 27” in your machine. Restart Unity.

Launch the Unity Project and click on Windows -> General -> Python Console.

Write the below program in the python editor and press Ctrl+A and click on Execute to run the program:
import UnityEngine
UnityEngine.Debug.Log(“Hello-The-World”) 

Follow this video for all the steps mentioned above for setting up Python Editor in Unity:
https://www.youtube.com/watch?v=3UOlN8FcNbE
 

Karting ML Tutorial:

Install Python 3.7.7 to run Tensorflow from here: https://www.python.org/downloads/release/python-377/

Select the checkbox of “Add Path” while installing the python.

Open the terminal and change the current working directory to the path of unity project and write below command: 
For Windows: python -m venv venv
For MacOS: python3 -m venv venv

To activate virtual environment type below command:
For Windows: venv\Scripts\activate
For MacOS: venv\bin\activate

Now finally to install the dependencies type below command: 
pip install -Iv mlagents==0.13.0

For training ML agents in unity you need to install the latest unity editor version 2021 and create a new project by selecting the template as Karting Microgame Template.
Available Karting ML Templates here: https://learn.unity.com/project/karting-template
You can create a new one by following this tutorial: https://www.youtube.com/watch?v=gYwWolRFt98
