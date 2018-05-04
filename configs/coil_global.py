

"""Detectron config system.

This file specifies default config options for Detectron. You should not
change values in this file. Instead, you should write a config file (in yaml)
and use merge_cfg_from_file(yaml_file) to load it and override the default
options.

Most tools in the tools directory take a --cfg option to specify an override
file and an optional list of override (key, value) pairs:
 - See tools/{train,test}_net.py for example code that uses merge_cfg_from_file
 - See configs/*/*.yaml for example config files

Detectron supports a lot of different model types, each of which has a lot of
different options. The result is a HUGE set of configuration options.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from ast import literal_eval
from utils import AttributeDict
import copy
import logging
import numpy as np
import os
import os.path as osp
import yaml


from logger.coil_logger import create_log

import imgauggpu as iag


class GlobalConfig(object):

    def __init__(self):

        self.param = AttributeDict()
        self.param.INPUT = AttributeDict()
        self.param.INPUT.SENSORS = {'rgb': (3, 88, 200)}
        self.param.INPUT.MEASUREMENTS = {'targets': (31)}
        self.param.INPUT.STEERING_DIVISION = [0.05, 0.05, 0.1, 0.3, 0.3, 0.1, 0.05, 0.05]
        self.param.INPUT.LABELS_DIVISION = [[0, 2, 5], [3], [4]]
        self.param.INPUT.AUGMENTATION = [iag.Add(0, 0)]
        self.param.INPUT.DATASET_NAME = 'None'



        #TODO: Why is misc misc ??
        self.param.MISC = AttributeDict
        self.param.TRAIN_EXPERIMENT_BATCH_NAME = "eccv"
        self.param.TRAIN_EXPERIMENT_NAME = "default"
        # TODO: not necessarily the configuration need to know about this
        self.param.PROCESS_NAME = "None"
        self.param.MISC.NUMBER_ITERATIONS = 50000
        self.param.MISC.NUMBER_FRAMES_FUSION = 1
        self.param.MISC.NUMBER_IMAGES_SEQUENCE = 1
        self.param.MISC.SEQUENCE_STRIDE = 1
        self.param.MISC.DATASET_SIZE = 2000
        #self.param.MISC.DATASET_SIZE





    def _check_integrity(self):


        pass



    def merge_with_yaml(self, yaml_filename):
        """Load a yaml config file and merge it into the global config object"""
        #with open(yaml_filename, 'r') as f:
        #    yaml_cfg = AttributeDict(yaml.load(f))
        #_merge_a_into_b(yaml_cfg, __C)
        #TODO: HERE IT IS NOT MUTABLE

        path_parts = os.path.split(yaml_filename)
        g_conf.param.TRAIN_EXPERIMENT_BATCH_NAME = os.path.split(path_parts[-2])[-1]
        g_conf.param.TRAIN_EXPERIMENT_NAME = path_parts[-1].split('.')[-2]

        print (g_conf.param.TRAIN_EXPERIMENT_BATCH_NAME)
        print (g_conf.param.TRAIN_EXPERIMENT_NAME)



    # TODO: is name really inside the configuration ??
    def set_type_of_process(self, type):
        """
        This function is used to set which is the type of the current process, test, train or val
        and also the details of each since there could be many vals and tests for a single
        experiment.

        NOTE: AFTER CALLING THIS FUNCTIONS THE CONFIGURATION CLOSES

        Args:
            type:

        Returns:

        """

        if self.param.PROCESS_NAME == "default":
            raise RuntimeError(" You should merge with some exp file before setting the type")

        if type == "train" or type == "validation":
            self.param.PROCESS_NAME = type + '_' + self.param.INPUT.DATASET_NAME
        #else:  # FOr the test case we join with the name of the experimental suite.

        create_log(g_conf.param.TRAIN_EXPERIMENT_BATCH_NAME,
                   g_conf.param.TRAIN_EXPERIMENT_NAME,
                   g_conf.param.PROCESS_NAME)

        self.param.immutable(True)





    def merge_with_parameters(self):
        pass

    def generate_name(self):
        pass






_g_conf = GlobalConfig()

g_conf = _g_conf






"""
# Random note: avoid using '.ON' as a config key since yaml converts it to True;
# prefer 'ENABLED' instead


# Miscelaneous configuration
__C.


# Configuration for training
__C.TRAIN = AttributeDict()

MISC:
  SAVE_MODEL_INTERVAL:
  BATCH_SIZE=120
  NUMBER_ITERATIONS:

LOGGING:

INPUT:
  DATASET:


TRAINING:


EVALUATION:
  NUMBER_BATCHES: 1800
  #NUMBER_IMAGES: 1800* # Number of images. ALL DERIVATED METRICS ARE COMPUTED INSIDE THE MODULUES

TEST:

"""



"""


# ---------------------------------------------------------------------------- #
# Deprecated options
# If an option is removed from the code and you don't want to break existing
# yaml configs, you can add the full config key as a string to the set below.
# ---------------------------------------------------------------------------- #
_DEPCRECATED_KEYS = set(
    {
        'FINAL_MSG',
        'MODEL.DILATION',
        'ROOT_GPU_ID',
        'RPN.ON',
        'TRAIN.BBOX_NORMALIZE_TARGETS_PRECOMPUTED',
        'TRAIN.DROPOUT',
        'USE_GPU_NMS',
        'TEST.NUM_TEST_IMAGES',
    }
)



# ---------------------------------------------------------------------------- #
# Renamed options
# If you rename a config option, record the mapping from the old name to the new
# name in the dictionary below. Optionally, if the type also changed, you can
# make the value a tuple that specifies first the renamed key and then
# instructions for how to edit the config file.
# ---------------------------------------------------------------------------- #
_RENAMED_KEYS = {
    'EXAMPLE.RENAMED.KEY': 'EXAMPLE.KEY',  # Dummy example to follow
    'MODEL.PS_GRID_SIZE': 'RFCN.PS_GRID_SIZE',
    'MODEL.ROI_HEAD': 'FAST_RCNN.ROI_BOX_HEAD',
    'MRCNN.MASK_HEAD_NAME': 'MRCNN.ROI_MASK_HEAD',
    'TRAIN.DATASET': (
        'TRAIN.DATASETS',
        "Also convert to a tuple, e.g., " +
        "'coco_2014_train' -> ('coco_2014_train',) or " +
        "'coco_2014_train:coco_2014_valminusminival' -> " +
        "('coco_2014_train', 'coco_2014_valminusminival')"
    ),
    'TRAIN.PROPOSAL_FILE': (
        'TRAIN.PROPOSAL_FILES',
        "Also convert to a tuple, e.g., " +
        "'path/to/file' -> ('path/to/file',) or " +
        "'path/to/file1:path/to/file2' -> " +
        "('path/to/file1', 'path/to/file2')"
    ),
    'TEST.SCALES': (
        'TEST.SCALE',
        "Also convert from a tuple, e.g. (600, ), " +
        "to a integer, e.g. 600."
    ),
    'TEST.DATASET': (
        'TEST.DATASETS',
        "Also convert from a string, e.g 'coco_2014_minival', " +
        "to a tuple, e.g. ('coco_2014_minival', )."
    ),
    'TEST.PROPOSAL_FILE': (
        'TEST.PROPOSAL_FILES',
        "Also convert from a string, e.g. '/path/to/props.pkl', " +
        "to a tuple, e.g. ('/path/to/props.pkl', )."
    ),
}

"""