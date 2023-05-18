Install Python 3.7.7 to run Tensorflow from here: https://www.python.org/downloads/release/python-377/

Select the checkbox of “Add Path” while installing the python.

Open the terminal and change the current working directory to the path of unity project and write below command: For Windows: python -m venv venv For MacOS: python3 -m venv venv

To activate virtual environment type below command: For Windows: venv\Scripts\activate For MacOS: venv\bin\activate

Now finally to install the dependencies type below command: pip install -Iv mlagents==0.13.0

For training ML agents in unity you need to install the latest unity editor version 2021 and create a new project by selecting the template as Karting Microgame Template. Available Karting ML Templates here: https://learn.unity.com/project/karting-template You can create a new one by following this tutorial: https://www.youtube.com/watch?v=gYwWolRFt98
