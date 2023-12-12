import json
import tempfile
from datetime import datetime as dt
from pathlib import Path
from urllib.parse import unquote_plus
from uuid import uuid4

import boto3  # type: ignore
import cv2

from libs.log import get_logger

log = get_logger(__name__)
s3 = boto3.client("s3")


def handler(event, _):
    """Resizes uploaded image"""
    begin_time = dt.utcnow()
    event_json_string = json.dumps(event)
    log.debug(f"request: {event_json_string}")

    bucket_name = event["Records"][0]["s3"]["bucket"]["name"]
    key = unquote_plus(event["Records"][0]["s3"]["object"]["key"], encoding="utf-8")
    log.info(f"Inputted Image: {bucket_name}/{key}")

    with tempfile.TemporaryDirectory() as tmpdir:
        save_path = Path(tmpdir).joinpath(Path(key).name)
        log.debug(f"tempdir `{tmpdir}` created.")
        # downloads target object
        with save_path.open("w+b") as f:
            log.debug(f"downloading...")
            s3.download_fileobj(bucket_name, key, f)
            log.debug(f"downloaded to `{f.name}` .")

        log.debug("processing image conversion...")
        org_image_path = cv2.imread(save_path.as_posix())
        gray_image_path = cv2.cvtColor(org_image_path, cv2.COLOR_RGB2GRAY)
        result_image = Path(tmpdir).joinpath(uuid4().hex).with_suffix(save_path.suffix)
        cv2.imwrite(result_image.as_posix(), gray_image_path)
        log.debug(f"processed image cerated to `{result_image}` .")
        log.debug(f"uploading...")
        target_key = f"result/{result_image.name}"
        s3.upload_file(
            Filename=result_image.as_posix(),
            Bucket=bucket_name,
            Key=target_key,
        )
        log.info(f"Uploaded to `{bucket_name}/{target_key}` .")
        log.debug(f"processed seconds: {(dt.utcnow()-begin_time).seconds}")

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "output": {
            "bucket": bucket_name,
            "key": target_key,
        },
    }
