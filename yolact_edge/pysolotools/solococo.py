from pysolotools.converters.solo2coco import SOLO2COCOConverter
from pysolotools.consumers import Solo
import os


# sequence_path = "./solo_4"
# output_path = "./output_data"

sequence_path =  "../../../../../../../media/adam/WinStorage/SyntheticHomes/solo_2"
output_path = "../../../../../../../media/adam/WinStorage/SyntheticHomes/output_2"
# sequence_path = "./validation_data_input"
# output_path = "./val_data_output"

# List of all the images in the sequence

# print(os.listdir(sequence_path))


solo = Solo(sequence_path)




dataset = SOLO2COCOConverter(solo)
dataset.convert(output_path=output_path)