from setuptools import find_packages, setup

# TODO: add versions for packages
setup(
    name="unity-dataset-visualizer",
    version="0.1",
    description="Visualizer for unity perception package for synthetic datasets",
    author="Unity Technologies",
    packages=find_packages(),
    python_requires=">=3.7,!=3.9.*",
    install_requires=[
        "Pillow>=8.1.0",
        "streamlit==0.84.1",
        # "gcsfs==0.7.1",
        "pyquaternion>=0.9.9",
        "datasetinsights==1.1.0",
        "PySide2==5.15.2",
    ],
    entry_points={"console_scripts": ["datasetvisualizer=datasetvisualizer.cli:main"]},
)
