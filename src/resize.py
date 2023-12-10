import json
import tempfile
from pathlib import PurePosixPath
from urllib.parse import unquote_plus
from uuid import uuid4

import boto3
import cv2

from libs.log import get_logger

log = get_logger(__name__)
s3 = boto3.client("s3")


def handler(event, _):
    """Resizes uploaded image"""
    event_json_string = json.dumps(event)
    log.info(f"request: {event_json_string}")

    bucket_name = event["Records"][0]["s3"]["bucket"]["name"]
    key = unquote_plus(event["Records"][0]["s3"]["object"]["key"], encoding="utf-8")
    bucket = s3.Bucket(bucket_name)
    log.info(f"Inputted Image: {bucket_name}/{key}")

    with tempfile.TemporaryDirectory() as tmpdir:
        save_path = PurePosixPath(tmpdir).joinpath(key)
        log.info(tmpdir)
        # downloads target object
        with save_path.open("wb") as f:
            bucket.download_fileobj(key, f)

        org_image = cv2.imread(save_path)
        gray_image = cv2.cvtColor(org_image, cv2.COLOR_RGB2GRAY)
        processed_obj_name = uuid4()
        suffix = save_path.suffix
        processed_image = (
            PurePosixPath(tmpdir).joinpath(processed_obj_name).joinpath(suffix)
        )
        cv2.imwrite(processed_image, gray_image)
        s3.upload_file(
            Filename=processed_image, Bucket=bucket, Key=f"grayed/{processed_image}"
        )

    return {"statusCode": 200, "headers": {"Content-Type": "text/plain"}}
