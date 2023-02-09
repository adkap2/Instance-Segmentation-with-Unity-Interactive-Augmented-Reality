import argparse
import json
import os
import sys
import subprocess
from typing import List, Tuple, Optional, Dict
import re

import streamlit as st

# import SessionState
import PIL.Image as Image
import streamlit.components.v1 as components

from datasetinsights.datasets.unity_perception import AnnotationDefinitions, MetricDefinitions
from datasetinsights.datasets.unity_perception.captures import Captures

import visualization.visualizers as v
import helpers.custom_components_setup as cc


def datamaker_dataset(path: str) -> Dict[int, Tuple[AnnotationDefinitions, MetricDefinitions, Captures, int, str]]:
    """ Reads the given path as a datamaker dataset

        Assumes that the given path contains a folder structure as follows:
        - path
            - urn_app_params folders
                - instance_#
                    - attempt_#
                        - Normal Perception dataset folder structure

        :param path: path to dataset
        :type path: str

        :return: Dictionary containing an entry for every instance, the key is the instance number, 
                each entry is a tuple as follows: (AnnotationDefinition, MetricDefiniton, Captures, number of captures, 
                absolute path to instance)
        :rtype: Dict[int, (AnnotationDefinitions, MetricDefinitions, Captures, int, str)]
    """
    instances = {}
    for app_param in [f.path for f in os.scandir(path) if f.is_dir()]:
        for instance in [g.path for g in os.scandir(app_param) if g.is_dir()]:
            if re.match(".*instance_[0-9]*", instance):
                instance_num = int(instance[instance.rfind("instance_") + len("instance_"):])
                for attempt in [h.path for h in os.scandir(instance) if h.is_dir()]:
                    if re.match(".*attempt_[0-9]*", attempt):
                        ann_def, metric_def, cap = load_perception_dataset(attempt)
                        if ann_def is not None:
                            instances[instance_num] = ann_def, metric_def, cap, len(
                                cap.captures.to_dict('records')), attempt

    if len(instances) > 0:
        return instances
    else:
        return None


@st.cache(show_spinner=True, allow_output_mutation=True)
def load_perception_dataset(path: str) -> Tuple[AnnotationDefinitions, MetricDefinitions, Captures]:
    """ Reads the given path as a normal Perception dataset and returns Dataset Insight objects that represent it

    :param path: root directory for a normal Perception dataset
    :type path: str

    :return: Annotations, Metrics and Captures for the given perception_dataset, if the dataset is invalid it returns
            (None, None, None)
    :rtype: (AnnotationDefinitions, MetricDefinitions, Captures)
    """
    try:
        ann_def = AnnotationDefinitions(path)
        metric_def = MetricDefinitions(path)
        cap = Captures(path)
        return ann_def, metric_def, cap
    except Exception:
        return None, None, None


def create_session_state_data(attribute_values: Dict[str, any]):
    """ Takes a dictionary of attributes to values to create the streamlit session_state object. 
    The values are the default values

    :param attribute_values: dictionary of session_state parameter to default values
    :type attribute_values: Dict[str, any]
    """
    for key in attribute_values:
        if key not in st.session_state:
            st.session_state[key] = attribute_values[key]


def create_sidebar_labeler_menu(available_labelers: List[str]) -> Dict[str, bool]:
    """
    Creates a streamlit sidebar menu that displays checkboxes and radio buttons to select which labelers to display

    :param available_labelers: List of strings representing labelers
    :type available_labelers: List[str]

    :return: Dictionary where keys are the available_labelers and values are bool representing if they have been chosen
    :rtype: Dict[str, bool]
    """

    # Note that here there is use of st.session_state._____existed_last_time this is used to workaround a streamlit bug
    # if this is removed then when user selects dataset with labeler X and turns it on then changes to dataset without
    # it then changes to a dataset with labeler X, labeler X appears as unselected but returns True as a value so acts
    # as if it was selected

    st.sidebar.markdown("# Visualize Labelers")
    labelers = {}
    if 'bounding box' in available_labelers:
        labelers['bounding box'] = st.sidebar.checkbox(
            "Bounding Boxes 2D") and st.session_state.bbox2d_existed_last_time
        st.session_state.bbox2d_existed_last_time = True
    else:
        st.session_state.bbox2d_existed_last_time = False

    if 'bounding box 3D' in available_labelers:
        labelers['bounding box 3D'] = st.sidebar.checkbox(
            "Bounding Boxes 3D") and st.session_state.bbox3d_existed_last_time
        st.session_state.bbox3d_existed_last_time = True
    else:
        st.session_state.bbox3d_existed_last_time = False

    if 'keypoints' in available_labelers:
        labelers['keypoints'] = st.sidebar.checkbox("Key Points") and st.session_state.keypoints_existed_last_time
        st.session_state.keypoints_existed_last_time = True
    else:
        st.session_state.keypoints_existed_last_time = False

    if 'instance segmentation' in available_labelers and 'semantic segmentation' in available_labelers:
        if st.sidebar.checkbox('Segmentation', False) and st.session_state.semantic_existed_last_time:
            selected_segmentation = st.sidebar.radio("Select the segmentation type:",
                                                     ['Semantic Segmentation', 'Instance Segmentation'],
                                                     index=0)
            if selected_segmentation == 'Semantic Segmentation':
                labelers['semantic segmentation'] = True
            elif selected_segmentation == 'Instance Segmentation':
                labelers['instance segmentation'] = True
        st.session_state.semantic_existed_last_time = True
    elif 'semantic segmentation' in available_labelers:
        labelers['semantic segmentation'] = st.sidebar.checkbox("Semantic Segmentation")
        st.session_state.semantic_existed_last_time = False
    elif 'instance segmentation' in available_labelers:
        labelers['instance segmentation'] = st.sidebar.checkbox("Instance Segmentation")
        st.session_state.semantic_existed_last_time = False
    else:
        st.session_state.semantic_existed_last_time = False
    if st.session_state.previous_labelers != labelers:
        st.session_state.labelers_changed = True
    else:
        st.session_state.labelers_changed = False
    st.session_state.previous_labelers = labelers
    return labelers


def display_number_frames(num_frames: int):
    """
    Creates a sidebar display for the number of frames in the selected dataset

    :param num_frames: Number of frames in the selected dataset
    :type num_frames: int
    """
    st.sidebar.markdown("### Number of frames: " + str(num_frames))


def preview_dataset(base_dataset_dir: str):
    """
    Adds streamlit components to the app to construct the dataset preview.

    :param base_dataset_dir: The directory that contains the perception dataset.
    :type base_dataset_dir: str
    """

    # Create state with default values
    create_session_state_data({
        'zoom_image': '-1',
        'start_at': '0',
        'num_cols': '3',
        'curr_dir': base_dataset_dir,

        'just_opened_zoom': True,
        'just_opened_grid': True,

        'bbox2d_existed_last_time': False,
        'bbox3d_existed_last_time': False,
        'keypoints_existed_last_time': False,
        'semantic_existed_last_time': False,

        'previous_labelers': {},
        'labelers_changed': False,
    })

    # Gets the latest selected directory
    base_dataset_dir = st.session_state.curr_dir

    # Display select dataset menu
    st.sidebar.markdown("# Select Dataset")
    if st.sidebar.button("Change Dataset"):
        folder_select()

    # Display name of dataset (Name of folder)
    dataset_name = base_dataset_dir
    folder_name = dataset_name.split('/')
    if len(folder_name) > 1:
        st.sidebar.markdown("# Current dataset:")
        st.sidebar.write(folder_name[-2])

    if dataset_name is not None:
        data_root = os.path.abspath(dataset_name)

        # Attempt to read data_root as a datamaker dataset
        instances = datamaker_dataset(data_root)

        # if it is not a datamaker dataset
        if instances is None:
            # Attempt to read as a normal perception dataset
            ann_def, metric_def, cap = load_perception_dataset(data_root)

            # if it fails to open as a normal percpetion dataset then consider it to be an invalid folder
            if ann_def is None:
                st.markdown("# Please select a valid dataset folder:")
                if st.button("Select dataset folder"):
                    folder_select()
                return

            display_number_frames(len(cap.captures.to_dict('records')))

            available_labelers = [a["name"] for a in ann_def.table.to_dict('records')]
            labelers = create_sidebar_labeler_menu(available_labelers)

            # zoom_image is negative if the application isn't in zoom mode
            index = int(st.session_state.zoom_image)
            if index >= 0:
                zoom(index, 0, ann_def, metric_def, cap, data_root, labelers)
            else:
                num_rows = 5
                grid_view(num_rows, ann_def, cap, data_root, labelers)

        # if it is a datamaker dataset
        else:
            display_number_frames(get_dataset_length_with_instances(instances))

            # zoom_image is negative if the application isn't in zoom mode
            index = int(st.session_state.zoom_image)
            if index >= 0:
                instance_key = get_instance_by_capture_idx(instances, index)
                offset = get_dataset_length_with_instances(instances, instance_key)
                ann_def, metric_def, cap, size, data_root = instances[instance_key]
                available_labelers = [a["name"] for a in ann_def.table.to_dict('records')]
                labelers = create_sidebar_labeler_menu(available_labelers)
                zoom(index, offset, ann_def, metric_def, cap, data_root, labelers)
            else:
                index = st.session_state.start_at
                num_rows = 5
                instance_key = get_instance_by_capture_idx(instances, index)
                ann_def, metric_def, cap, _, data_root = instances[instance_key]
                available_labelers = [a["name"] for a in ann_def.table.to_dict('records')]
                labelers = create_sidebar_labeler_menu(available_labelers)
                grid_view_instances(num_rows, instances, labelers)
    else:
        st.markdown("# Please select a valid dataset folder:")
        if st.button("Select dataset folder"):
            folder_select()


def get_instance_by_capture_idx(
        instances: Dict[int, Tuple[AnnotationDefinitions, MetricDefinitions, Captures, int, str]], index: int) \
        -> int:
    """ Gets the instance in instances that contains the given capture index

    :param instances: Dictionary of instances
    :type instances: Dict[int, Tuple[AnnotationDefinitions, MetricDefinitions, Captures, int, str]]
    :param index: Capture index that we want
    :type index: int

    :return: key in dictionary
    :rtype: int
    """
    total = 0
    keys = list(instances.keys())
    keys.sort()
    for key in keys:
        total = total + instances[key][3]
        if int(index) <= total - 1:
            return key


def get_dataset_length_with_instances(
        instances: Dict[int, Tuple[AnnotationDefinitions, MetricDefinitions, Captures, int, str]],
        until_instance: int = -1) -> \
        int:
    """ Gets the total length of a dataset that goes over multiple instances (aka. Datamaker dataset)
    optionally you can specify until which instance you want to count 
    (the order is based by the natural ordering of keys)

    :param instances: Dictionary of instances
    :type instances: Dict[int, Tuple[AnnotationDefinitions, MetricDefinitions, Captures, int, str]]
    :param until_instance: optional, will stop counting when it reaches the specified instance (non-inclusive)
    :type until_instance: int
    :return: length
    :rtype: int
    """
    total = 0
    keys = list(instances.keys())
    keys.sort()
    for key in keys:
        if 0 <= until_instance <= key:
            break
        total = total + instances[key][3]
    return total


def get_annotation_id(ann_def: AnnotationDefinitions, name: str) -> Optional[str]:
    """ gets annotation definition id of the specified annotation

    :param ann_def: Annotations in dataset
    :type ann_def: AnnotationDefinitions
    :param name: Name of the annotation we want the id of
    :type name: str
    :return: annotation definition id
    :rtype: str
    """
    for idx, a in enumerate(ann_def.table.to_dict('records')):
        if a["name"] == name:
            return a["id"]
    return None


def get_annotation_index(ann_def: AnnotationDefinitions, name: str) -> int:
    """ gets annotation definition index of the specified annotation

    :param ann_def: Annotations in dataset
    :type ann_def: AnnotationDefinitions
    :param name: Name of the annotation we want the id of
    :type name: str
    :return: index
    :rtype: int
    """
    for idx, a in enumerate(ann_def.table.to_dict('records')):
        if a["name"] == name:
            return idx
    return -1


def custom_compare_filenames(filenames):
    for i in range(len(filenames)):
        filenames[i] = int(os.path.basename(filenames[i])[4:-4])
    return filenames


def get_image_with_labelers(
        index: int,
        ann_def: AnnotationDefinitions,
        cap: Captures,
        data_root: str,
        labelers_to_use: Dict[str, bool],
        max_size: int = 500) -> Image:
    """ Creates a PIL image of the capture at index that has all the labelers_to_use visualized

    :param index: The index of the frame we want
    :type index: int
    :param ann_def: The Annotations for the dataset
    :type ann_def: AnnotationsDefinitions
    :param cap: The Captures for the dataset
    :type cap: Captures
    :param data_root: The root of the 
    :type data_root: str
    :param labelers_to_use: Dictionary containing keys for the name of every labeler available in the given dataset
                            and the corresponding value is a boolean representing whether or not to display it
    :type labelers_to_use: Dict[str, bool]
    :param max_size: Optional (Default: 500), determines the maximum size of width and height of the created image
                     Useful for optimizing. In the visualizer, if the images were full sized: the browser would take too
                     much time to display them
    :type max_size: int
    :return: The image with the labelers
    :rtype: PIL.Image
    """
    captures = cap.filter(def_id=ann_def.table.to_dict('records')[0]["id"])
    captures = captures.sort_values(by='filename', key=custom_compare_filenames).reset_index(drop=True)
    capture = captures.loc[index, "filename"]
    filename = os.path.join(data_root, capture)
    image = Image.open(filename)

    if 'bounding box' in labelers_to_use and labelers_to_use['bounding box']:
        bounding_box_definition_id = get_annotation_id(ann_def, 'bounding box')
        bb_captures = cap.filter(def_id=bounding_box_definition_id)
        bb_captures = bb_captures.sort_values(by='filename', key=custom_compare_filenames).reset_index(drop=True)
        init_definition = ann_def.get_definition(bounding_box_definition_id)
        label_mappings = {
            m["label_id"]: m["label_name"] for m in init_definition["spec"]
        }
        image = v.draw_image_with_boxes(
            image,
            index,
            bb_captures,
            label_mappings,
        )

    if 'keypoints' in labelers_to_use and labelers_to_use['keypoints']:
        keypoints_definition_id = get_annotation_id(ann_def, 'keypoints')
        kp_captures = cap.filter(def_id=keypoints_definition_id)
        kp_captures = kp_captures.sort_values(by='filename', key=custom_compare_filenames).reset_index(drop=True)
        annotations = kp_captures.loc[index, "annotation.values"]
        templates = ann_def.table.to_dict('records')[get_annotation_index(ann_def, 'keypoints')]['spec']
        v.draw_image_with_keypoints(image, annotations, templates)

    if 'bounding box 3D' in labelers_to_use and labelers_to_use['bounding box 3D']:
        bounding_box_3d_definition_id = get_annotation_id(ann_def, 'bounding box 3D')
        box_captures = cap.filter(def_id=bounding_box_3d_definition_id)
        box_captures = box_captures.sort_values(by='filename', key=custom_compare_filenames).reset_index(drop=True)
        annotations = box_captures.loc[index, "annotation.values"]
        sensor = box_captures.loc[index, "sensor"]
        image = v.draw_image_with_box_3d(image, sensor, annotations, None)

    # bounding boxes and keypoints are depend on pixel coordinates so for now the thumbnail optimization applies only to
    # segmentation
    # TODO Make it so that bounding boxes and keypoints can be visualized at a lower resolution

    image.thumbnail((max_size, max_size))
    if 'semantic segmentation' in labelers_to_use and labelers_to_use['semantic segmentation']:
        semantic_segmentation_definition_id = get_annotation_id(ann_def, 'semantic segmentation')

        seg_captures = cap.filter(def_id=semantic_segmentation_definition_id)
        seg_captures = seg_captures.sort_values(by='filename', key=custom_compare_filenames).reset_index(drop=True)
        seg_filename = os.path.join(data_root, seg_captures.loc[index, "annotation.filename"])
        seg = Image.open(seg_filename)
        seg.thumbnail((max_size, max_size))

        image = v.draw_image_with_segmentation(
            image, seg
        )

    if 'instance segmentation' in labelers_to_use and labelers_to_use['instance segmentation']:
        instance_segmentation_definition_id = get_annotation_id(ann_def, 'instance segmentation')

        inst_captures = cap.filter(def_id=instance_segmentation_definition_id)
        inst_captures = inst_captures.sort_values(by='filename', key=custom_compare_filenames).reset_index(drop=True)
        inst_filename = os.path.join(data_root, inst_captures.loc[index, "annotation.filename"])
        inst = Image.open(inst_filename)
        inst.thumbnail((max_size, max_size))

        image = v.draw_image_with_segmentation(
            image, inst
        )

    return image


def folder_select():
    """ Runs a subprocess that opens a file dialog to select a new directory, this will update st.session_state.curr_dir
    """
    output = subprocess.run(
        [sys.executable, os.path.join(os.path.dirname(os.path.realpath(__file__)), "helpers/folder_explorer.py")],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )
    stdout = str(os.path.abspath(str(output.stdout).split("\'")[1]))
    if stdout[-4:] == "\\r\\n":
        stdout = stdout[:-4]
    elif stdout[-2:] == '\\n':
        stdout = stdout[:-2]
    proj_root = stdout.replace("\\", "/") + "/"

    st.session_state.curr_dir = proj_root
    st.experimental_rerun()


def create_grid_view_controls(num_rows: int, dataset_size: int) -> Tuple[int, int]:
    """ Creates the controls for grid view

    :param num_rows: number of rows to display
    :type num_rows: int
    :param dataset_size: The size of the dataset
    :type dataset_size: int
    :return: Returns the number of columns and the index at which the grid must start
    :rtype: Tuple[int, int]
    """
    header = st.beta_columns([2 / 3, 1 / 3])

    num_cols = header[1].slider(label="Frames per row: ", min_value=1, max_value=5, step=1,
                                value=int(st.session_state.num_cols))
    if not num_cols == st.session_state.num_cols:
        st.session_state.num_cols = num_cols
        st.experimental_rerun()

    with header[0]:
        new_start_at = int(cc.item_selector(int(st.session_state.start_at), num_cols * num_rows,
                                            dataset_size))
        if not new_start_at == st.session_state.start_at and not st.session_state.just_opened_grid:
            st.session_state.start_at = new_start_at

        st.session_state.just_opened_grid = False
        start_at = int(st.session_state.start_at)

    components.html("""<hr style="height:2px;border:none;color:#AAA;background-color:#AAA;" /> """, height=10)
    return num_cols, start_at


def create_grid_containers(num_rows: int, num_cols: int, start_at: int, dataset_size: int) -> List[any]:
    """ Creates the streamlit containers that will hold the images in a grid, this must happen before placing the images
    so that when clicking on "Expand frame" it doesn't need to reload every image before opening in zoom view

    :param num_rows: Number of rows
    :type num_rows: int
    :param num_cols: Number of columns
    :type num_cols: int
    :param start_at: Index at which the grid starts
    :type start_at: int
    :param dataset_size: Size of the dataset
    :type dataset_size: int
    :return: list of the containers in order from left to right, up to down
    :rtype: List[any]
    """
    cols = st.beta_columns(num_cols)
    containers = [None] * (num_cols * num_rows)
    for i in range(start_at, min(start_at + (num_cols * num_rows), dataset_size)):
        containers[i - start_at] = cols[(i - (start_at % num_cols)) % num_cols].beta_container()
        # container.write("Frame #" + str(i))
        with containers[i - start_at]:
            components.html(
                """<p style="margin-top:35px;margin-bottom:0px;font-family:IBM Plex Sans, sans-serif"></p>""",
                height=35)
        expand_image = containers[i - start_at].button(label="Expand Frame", key="exp" + str(i))
        if expand_image:
            st.session_state.zoom_image = i
            st.session_state.just_opened_zoom = True
            st.experimental_rerun()
    return containers


def grid_view(num_rows: int, ann_def: AnnotationDefinitions, cap: Captures, data_root: str, labelers: Dict[str, bool]):
    """ Creates the grid view streamlit components

    :param num_rows: Number of rows
    :type num_rows: int
    :param ann_def: Annotations for dataset
    :type ann_def: AnnotationDefinitions
    :param cap: Captures for dataset
    :type cap: Captures
    :param data_root: Path to dataset root
    :type data_root: str
    :param labelers: Dictionary containing keys for the name of every labeler available in the given dataset
                     and the corresponding value is a boolean representing whether or not to display it
    :type labelers: Dict[str, bool]
    """
    num_cols, start_at = create_grid_view_controls(num_rows, len(cap.captures.to_dict('records')))

    containers = create_grid_containers(num_rows, num_cols, start_at, len(cap.captures.to_dict('records')))

    for i in range(start_at, min(start_at + (num_cols * num_rows), len(cap.captures.to_dict('records')))):
        image = get_image_with_labelers(i, ann_def, cap, data_root, labelers, max_size=get_resolution_from_num_cols(num_cols))
        containers[i - start_at].image(image, caption=str(i), use_column_width=True)


def get_resolution_from_num_cols(num_cols):
    if num_cols == 5:
        return 300
    else:
        return (6 - num_cols) * 200


def grid_view_instances(
        num_rows: int,
        instances: Dict[int, Tuple[AnnotationDefinitions, MetricDefinitions, Captures, int, str]],
        labelers: Dict[str, bool]):
    """ Creates the grid view streamlit components when using a Datamaker dataset

    :param num_rows: Number of rows
    :type num_rows: int
    :param instances: Dictionary of instances
    :type instances: Dict[int, Tuple[AnnotationDefinitions, MetricDefinitions, Captures, int, str]]
    :param labelers: Dictionary containing keys for the name of every labeler available in the given dataset
                     and the corresponding value is a boolean representing whether or not to display it
    :type labelers: Dict[str, bool]
    """
    dataset_size = get_dataset_length_with_instances(instances)
    num_cols, start_at = create_grid_view_controls(num_rows, dataset_size)

    containers = create_grid_containers(num_rows, num_cols, start_at, dataset_size)

    for i in range(start_at, min(start_at + (num_cols * num_rows), dataset_size)):
        instance_key = get_instance_by_capture_idx(instances, i)
        ann_def, metric_def, cap, size, data_root = instances[instance_key]
        image = get_image_with_labelers(i - get_dataset_length_with_instances(instances, instance_key), ann_def,
                                        cap, data_root, labelers, max_size=(6 - num_cols) * 150)
        containers[i - start_at].image(image, caption=str(i), use_column_width=True)


def zoom(index: int,
         offset: int,
         ann_def: AnnotationDefinitions,
         metrics_def: MetricDefinitions,
         cap: Captures,
         data_root: str,
         labelers: Dict[str, bool]):
    """ Creates streamlit components for Zoom in view

    :param index: Index of the image
    :type index: int
    :param offset: Is how much the index needs to be offset, this is only needed to 
                   handle multiple instances (Datamaker datasets)
    :type offset: int
    :param ann_def: Annotations for Dataset
    :type ann_def: AnnotationsDefinitions
    :param metrics_def: Metrics for the dataset
    :type metrics_def: MetricsDefinitions
    :param cap: Captures for Dataset
    :type cap: Captures
    :param data_root: Path to dataset (Note that when using instances this is the path to the instance the index is in)
    :type data_root: str
    :param labelers: Dictionary containing keys for the name of every labeler available in the given dataset
                     and the corresponding value is a boolean representing whether or not to display it
    :type labelers: Dict[str, bool]
    """
    dataset_size = len(cap.captures.to_dict('records'))

    st.session_state.start_at = index
    st.session_state.zoom_image = index

    if st.button('< Back to Grid view'):
        st.session_state.zoom_image = -1
        st.session_state.just_opened_grid = True
        st.experimental_rerun()

    header = st.beta_columns([2 / 3, 1 / 3])
    with header[0]:
        new_index = cc.item_selector_zoom(index, dataset_size + offset)
        if not new_index == index and not st.session_state.just_opened_zoom and not st.session_state.labelers_changed:
            st.session_state.zoom_image = new_index
            st.session_state.start_at = index
            st.experimental_rerun()

    st.session_state.start_at = index
    st.session_state.zoom_image = index
    st.session_state.just_opened_zoom = False

    components.html("""<hr style="height:2px;border:none;color:#AAA;background-color:#AAA;" /> """, height=30)

    index = index - offset
    image = get_image_with_labelers(index, ann_def, cap, data_root, labelers, max_size=2000)

    st.image(image, use_column_width=True)
    layout = st.beta_columns(2)
    layout[0].title("Captures Metadata")

    captures_dir = None
    for directory in os.walk(data_root):
        name = str(directory[0]).replace('\\', '/').split('/')[-1]
        if name.startswith("Dataset") and \
                "." not in name[1:] and \
                os.path.abspath(data_root) != os.path.abspath(directory[0]):
            captures_dir = os.path.abspath(directory[0])
            break

    path_to_captures = os.path.join(os.path.abspath(captures_dir), "captures_000.json")
    json_file = json.load(open(path_to_captures, "r"))
    num_captures_per_file = len(json_file["captures"])

    file_num = index // num_captures_per_file
    postfix = ('000' + str(file_num))
    postfix = postfix[len(postfix) - 3:]
    path_to_captures = os.path.join(os.path.abspath(captures_dir), "captures_" + postfix + ".json")
    with layout[0]:
        json_file = json.load(open(path_to_captures, "r"))
        capture = json_file['captures'][index % num_captures_per_file]
        st.write(capture)

    layout[1].title("Metrics Metadata")
    metrics = []
    for i in os.listdir(captures_dir):
        path_to_metrics = os.path.join(captures_dir, i)
        if os.path.isfile(path_to_metrics) and 'metrics_' in i and 'definitions' not in i:
            json_file = json.load(open(path_to_metrics))
            metrics.extend(json_file['metrics'])
    with layout[1]:
        for metric in metrics:
            if metric['sequence_id'] == capture['sequence_id'] and metric['step'] == capture['step']:
                for metric_def in metrics_def.table.to_dict('records'):
                    if metric_def['id'] == metric['metric_definition']:
                        st.markdown("## " + metric_def['name'])
                st.write(metric)


def preview_app(args):
    """
    Starts the dataset preview app.

    :param args: Arguments for the app, such as dataset
    :type args: Namespace
    """
    preview_dataset(args["data"])


if __name__ == "__main__":

    # This needs to be the first streamlit command
    st.set_page_config(layout="wide")
    # removes the default zoom button on images
    st.markdown('<style>button.css-enefr8{display: none}</style>', unsafe_allow_html=True)

    parser = argparse.ArgumentParser()
    parser.add_argument("data", type=str)
    args = parser.parse_args()
    if os.path.isdir(args.data):
        preview_app({"data": args.data})
    else:
        preview_app({"data": ""})
