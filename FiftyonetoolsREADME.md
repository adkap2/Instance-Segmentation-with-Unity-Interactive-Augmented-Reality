# Github Source Link: https://github.com/voxel51/fiftyone

# Website: https://voxel51.com/fiftyone/

# Introduction

FiftyOne is a Python package and web application designed for computer vision and machine learning workflows. It provides a range of tools and functionalities for working with image and video datasets, including data exploration, visualization, analysis, and labeling.

FiftyOne can be used to load and visualize large datasets, perform dataset exploratory analysis, and preprocess data for training. It also provides an interactive labeling interface that allows for manual annotation of images and videos, as well as semi-automated labeling using active learning methods. Additionally, FiftyOne includes functionality for creating data splits, managing data versions, and exporting datasets to different formats.

FiftyOne is particularly useful for deep learning applications in computer vision, such as image classification, object detection, and segmentation. It is designed to streamline the data preparation and labeling process, allowing users to focus on building and refining their models.

In this case, the tool is used to modify the data generated with the Unity SyntheticHomes executable to be trained with the YOLACT Instance Segmentation model.  

FiftyOne provides a range of tools for curating high-quality image datasets, including the ability to modify COCO-style annotations, identify and correct errors in existing annotations, select and modify specific object categories, and visualize the data. These tools are particularly useful for preparing datasets for machine learning and computer vision applications, where accurate and high-quality annotations are critical for model performance.

FiftyOne's annotation tools allow users to manually label images with bounding boxes, segmentation masks, and keypoints, as well as leverage semi-automated labeling using active learning techniques. FiftyOne also includes a variety of visualization tools, such as the ability to display images with annotations overlaid, to help users better understand their datasets and ensure they are properly labeled.

Overall, FiftyOne is designed to streamline the process of data curation and preparation for machine learning and computer vision applications, allowing users to focus on building and refining their models.

# Installations and Converting from SOLO to COCO format

Note1: This code was performed and tested using macOS Monterey Version 12.6 and the application used to run the code is VS Code. The Python version used here is 3.9.16 but it works on any python > 3.8.8 version.

Note2: If original dataset is in SOLO format, pysolotools is necessary to convert to COCO format

1. Create one folder named solo2
2. Place the  “data” folder inside solo2, this data folder is the same folder of the images generated from SyntheticHome image generator. Create a new python notebooknamed “solo2coco.ipynb” in the solo2 folder. In VS Code open the solo2 folder and open “solo2coco.ipynb” file.
3. In the VS Code terminal install all the dependencies based on your python version
4. Install pysolotools: pip install pysolotools
      Install FiftyOne: pip install fiftyone
5. Imports:
      from pysolotools.converters.solo2coco import SOLO2COCOConverter
      from pysolotools.consumers import Solo
      import os
6. Set the data input and output path
      input_path =  "/path/to/data/"
      output_path = "/path/to/export/data"
7. Create a solo object from data
      solo = Solo(input_path)
8. Convert to COCO and export data
      dataset = SOLO2COCOConverter(solo)
      dataset.convert(output_path=output_path)
      
# Viewing the Dataset with FiftyOne

1. Create FiftyOne Python Notebook in the same solo2 folder with name “fiftyone_data.ipynb”
2. Open that python notebook and import necessary packages
    import fiftyone as fo
    import fiftyone.zoo as foz
    from fiftyone import ViewField as F
    import os
3. Load the Dataset
Note: Path to data in the below code snippet is the path for the images file created inside the output_data folder which was created inside solo2 folder.
Path to annotations in the below code snippet is the path for the “instances.json” file created inside the output_data folder which was created inside solo2 folder.
cwd = os.getcwd()
data_path = cwd + "/path/to/data"
labels_path = cwd + "path/to/annotations"
dataset_type = fo.types.COCODetectionDataset

dataset = fo.Dataset.from_dir(
   data_path=data_path,
   labels_path=labels_path,
   dataset_type = dataset_type,
)

4. View the Dataset with FiftyOne Viewer
    session = fo.launch_app(dataset)
5. Select segmentations and filter by Label to limit viewable annotations.

# Modifying the Data with FiftyOne

1. Map Specific Data Labels to intended training categories


        dataset1=dataset


        dataset1 = dataset1.map_labels("segmentations", {"Bed": "Bed", "Bed_Bunk": "Bed"})
        dataset1 = dataset1.map_labels("segmentations", {"Bench": "Bench"})
        dataset1 = dataset1.map_labels("segmentations", {"Chair_Lounge": "Chair", "Chair_Club": "Chair", "Chair_Arm": "Chair", "Chair_Dining": "Chair"})
        dataset1 = dataset1.map_labels("segmentations", {"Door_Sliding_Glass": "Door", "Door_Sliding_Wood": "Door", "Door_lockset": "Door", "Door_casing": "Door", "Door_casing_flat": "Door"})
        dataset1 = dataset1.map_labels("segmentations", {"Appliance_microwave": "Microwave", "Appliance_refrigerator": "Refrigerator", "Appliance_refrigerator_top-freezer": "Refrigerator"})
        dataset1 = dataset1.map_labels("segmentations", {"Sofa": "Sofa"})
        dataset1 = dataset1.map_labels("segmentations", {"Table_End": "Table", "Table_Dining": "Table", "Table_Console": "Table", "Table_Coffee": "Table"})

2. Specify Categories intended for training
        dataset1 = dataset1.filter_labels("segmentations", F("label").is_in(["Bed", "Bench", "Chair", "Door", "Microwave", "Refrigerator", "Sofa", "Table"]))
        
3. Exclude Detections and Keypoints
        dataset = dataset.exclude_fields("detections").exclude_fields("keypoints")
        
4. Launch Session to view modifications
        session = fo.launch_app(dataset1)
5. Split data to train and validation set
        import fiftyone.utils.random as four
        view1, view2 = four.random_split(dataset1, [0.8, 0.2])
6. Export Dataset
        view1.export(
   export_dir=cwd + "/path/to/train",
   dataset_type=fo.types.COCODetectionDataset,
   label_field="segmentations",
   overwrite=True,
  )

  view2.export(
     export_dir=cwd + "/path/to/val",
     dataset_type=fo.types.COCODetectionDataset,
     label_field="segmentations",
     overwrite=True,
  )
  
  # Citation
[1]
B. E. Moore and J. J. Corso, "FiftyOne," GitHub. Note: https://github.com/voxel51/fiftyone, 2020. [Online]. Available: https://github.com/voxel51/fiftyone. [Accessed: Mar. 02, 2023].







