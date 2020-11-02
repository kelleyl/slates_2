"""
This module loads slate annotations from a hard coded file, loads the corresponding video
and saves the frame annotated as slate_start and the frame 15 frames before the frame
designated as slate_end.
"""
import csv
import os
import random
from random import sample

import cv2
from timecode import Timecode

import utils

DATA_DIR = "/data/clams/wgbh/wrvr/Videos_for_slate_training"

SLATE_DIR = "./data/raw/slate_images"
NON_SLATE_DIR = "./data/raw/non-slate-images"
METADATA_FILE_PATH = "./data/annotations/_videos_with_slates.csv"

random.seed(42)

# create data folders
try:
    if not os.path.exists(SLATE_DIR):
        os.makedirs(SLATE_DIR)
    if not os.path.exists(NON_SLATE_DIR):
        os.makedirs(NON_SLATE_DIR)
except OSError:
    raise Exception("Error: Creating directory for data")


def save_frame(video_cap, frame_number, output_directory, dryrun=False):
    # dryrun=True #uncomment this line to just do a dry run
    name = f"{output_directory}/{guid}_{str(frame_number)}.jpg"
    video_cap.set(1, frame_number)
    ret, frame = video_cap.read()
    if ret:
        if dryrun:
            print(f"DRYRUN: Creating...{name}")
        else:
            print(f"Creating...{name}")
            cv2.imwrite(name, frame)


def clean_strings(reader):
    """
    takes a csv dict reader object and iterates through removing leading and
    trailing whitespace from each key and value
    :param reader: csv.DictReader object
    :return: list of dictionaries
    """
    result = []
    for d in reader:
        clean = {k.strip(): v.strip() for k, v in d.items()}
        result.append(clean)
    return result


def save_random_frames(video_cap, count=100, exclude_start=None, exclude_end=None):
    """
    :param video_cap: cv2 video capture object from which to select and save frames
    :param count: number of frames to save
    :param exclude_start: start of frame segment to exclude from selection
    :param exclude_end: end of frame segment to exclude from selection
    :return: None
    """
    video_frame_count = int(video_cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if (
        video_frame_count < 1
    ):  # sometimes reading the prop doesnt work, so we manually count instead
        video_frame_count = utils.get_frame_count(video_cap)
    result_frame_numbers = sample(
        [
            frame_number
            for frame_number in range(0, video_frame_count)
            if frame_number not in range(exclude_start, exclude_end + 30)
        ],
        k=count,
    )
    for frame_number in result_frame_numbers:
        save_frame(video_cap, frame_number, NON_SLATE_DIR)
    return


if __name__ == "__main__":
    with open(METADATA_FILE_PATH, "r") as md_csv:
        reader = clean_strings(csv.DictReader(md_csv))
        for item in reader[:291]: #only the first 291 are annotated
            if item["Slate End"]:
                start_t = Timecode("30", item["Slate Start"])
                end_t = Timecode("30", item["Slate End"])

                # # Read the video from specified path
                guid = item["GUID"]
                print(guid, start_t.frames, end_t.frames)

                cap = cv2.VideoCapture(os.path.join(DATA_DIR, f"{guid}.h264.mp4"))
                save_frame(cap, start_t.frame_number, SLATE_DIR)
                # save_frame(cap, end_t.frame_number - 15, SLATE_DIR)
                save_random_frames(
                    cap, exclude_start=start_t.frames, exclude_end=end_t.frames
                )
                # Release all space and windows once done
                cap.release()
