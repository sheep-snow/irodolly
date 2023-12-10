# https://github.com/yKesamaru/Estimate_face_orientation - 頭部姿勢推定を簡易実装する
# https://yoppa.org/mit-design4-22/14113.html - MediaPipeで遊んでみる
# https://developers.google.com/mediapipe/solutions/vision/pose_landmarker#get_started - Pose Detection Basics

import json
import tempfile
from pathlib import PurePosixPath
from urllib.parse import unquote_plus

import boto3  # type: ignore
import cv2

from libs.log import get_logger

log = get_logger(__name__)
s3 = boto3.client("s3")

import numpy as np
from mediapipe import solutions  # type: ignore
from mediapipe.framework.formats import landmark_pb2  # type: ignore


def draw_landmarks_on_image(rgb_image, detection_result):
    pose_landmarks_list = detection_result.pose_landmarks
    annotated_image = np.copy(rgb_image)

    # Loop through the detected poses to visualize.
    for idx in range(len(pose_landmarks_list)):
        pose_landmarks = pose_landmarks_list[idx]

        # Draw the pose landmarks.
        pose_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
        pose_landmarks_proto.landmark.extend(
            [
                landmark_pb2.NormalizedLandmark(
                    x=landmark.x, y=landmark.y, z=landmark.z
                )
                for landmark in pose_landmarks
            ]
        )
        solutions.drawing_utils.draw_landmarks(
            annotated_image,
            pose_landmarks_proto,
            solutions.pose.POSE_CONNECTIONS,
            solutions.drawing_styles.get_default_pose_landmarks_style(),
        )
    return annotated_image


def handler(event, _):
    event_json_string = json.dumps(event)
    log.info(f"request: {event_json_string}")

    bucket_name = event["Records"][0]["s3"]["bucket"]["name"]
    key = unquote_plus(event["Records"][0]["s3"]["object"]["key"], encoding="utf-8")
    bucket = s3.Bucket(bucket_name)
    log.info(f"Inputted Image: {bucket_name}/{key}")

    with tempfile.TemporaryDirectory() as tmpdir:
        log.debug(f"Tempdir `{tmpdir}` created.")
        # downloads target object
        save_path = PurePosixPath(tmpdir).joinpath(key)
        log.debug("")
        with save_path.open("wb") as f:
            bucket.download_fileobj(key, f)
            log.debug(f"The object `{key}` downloaded to {str(save_path)}.")

        # uploads processed image to the bucket
        with save_path.open("rb") as f:
            s3.upload_file(
                Filename=save_path,
                Bucket=bucket,
                Key=f"pose_detected/{processed_image}",
            )
            bucket.download_fileobj(key, f)
            log.debug(f"The object `{key}` downloaded to {str(save_path)}.")

    draw_landmarks_on_image({}, {})

    return {"statusCode": 200, "headers": {"Content-Type": "text/plain"}}
