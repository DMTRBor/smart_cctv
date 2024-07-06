import os
import cv2
import numpy as np
import cvlib as cv
from cvlib.object_detection import draw_bbox


###############################################
OPEN_KERNEL_SIZE = (3,3)
YOLO_MIN_CONFIDENCE = 0.2
YOLO_NMS_THRESHOLD = 0.5
###############################################


def background_subtractor():
    # Mixture Of Gaussians
    foreground_model = cv2.createBackgroundSubtractorMOG2()
    return foreground_model


def noise_filtering(frame):
    # use morphological "Open" operation
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, OPEN_KERNEL_SIZE)
    denoised_frame = cv2.morphologyEx(np.float32(frame),
                                      cv2.MORPH_OPEN,
                                      kernel)
    return denoised_frame


def filter_connected_components(frame, threshold):
    _, labeled_im = cv2.connectedComponents(np.array(frame > 0, np.uint8))

    R = np.zeros(labeled_im.shape) < 0
    unique_labels = np.unique(labeled_im.flatten())

    for label in unique_labels:
        if label != 0:
            filter_labels = labeled_im==label
            if np.sum(filter_labels) > threshold:
                R = R | filter_labels

    return np.float32(255 * R)


def run_yolo(frame, yolo_model='yolov3-tiny'):
    bbox, labels, conf = cv.detect_common_objects(frame,
                                                  confidence=YOLO_MIN_CONFIDENCE,
                                                  nms_thresh=YOLO_NMS_THRESHOLD,
                                                  model=yolo_model)
    frame = draw_bbox(frame, bbox, labels, conf, write_conf=True)
    return frame


def save_frames(frames_arr, frame_counter, threshold, output_path, is_run_yolo=True, image_format='.jpg'):
    if len(frames_arr) >= threshold:
        frame_number = 1

        for frame in frames_arr:
            im_name = str(frame_counter) + '_' + str(frame_number) + image_format
            final_output_path = os.path.join(output_path, im_name)

            if is_run_yolo:
                frame = run_yolo(frame)

            cv2.imwrite(final_output_path, frame)
            frame_number += 1
