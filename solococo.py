from pysolotools.converters.solo2coco import SOLO2COCOConverter
from pysolotools.consumers import Solo
import os


sequence_path =  "C:\\Users\\ryan\\Documents\\SyntheticHomes\\Images_Output\\solo"
output_path = "C:\\Users\\ryan\\Documents\\SyntheticHomes\\Images_Output\\output1"

# List of all the images in the sequence

# print(os.listdir(sequence_path))


solo = Solo(sequence_path)

dataset = SOLO2COCOConverter(solo)
dataset.convert(output_path=output_path)