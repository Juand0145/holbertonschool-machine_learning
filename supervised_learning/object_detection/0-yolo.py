#!/usr/bin/env python3
"""File that contains the class Yolo"""
import tensorflow.keras as K


class Yolo:
    """Class YOLO(You only look once)"""

    def __init__(self, model_path, classes_path, class_t, nms_t, anchors):
        """
        model_path is the path to where a Darknet Keras model is stored.
        classes_path is the path to where the list of class names used for
        the Darknet model, listed in order of index, can be found.
        class_t is a float representing the box score threshold for the initial filtering step.
        nms_t is a float representing the IOU threshold for non-max suppression.
        anchors is a numpy.ndarray of shape (outputs, anchor_boxes, 2) containing all of the anchor boxes:
            outputs is the number of outputs (predictions) made by the Darknet model
            anchor_boxes is the number of anchor boxes used for each prediction
            2 => [anchor_box_width, anchor_box_height]
        """
        model = K.models.load_model(model_path)

        with open(classes_path, "r") as classes_file:
            classes = [line.strip() for line in classes_file.readlines()]

        self.model = model
        self.class_names = classes
        self.class_t = class_t
        self.nms_t = nms_t
        self.anchors = anchors
