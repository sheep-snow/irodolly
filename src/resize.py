import json

from libs.log import get_logger

log = get_logger(__name__)


def handler(event, context):
    """Resizes uploaded image"""
    event_json_string = json.dumps(event)
    # TODO implement it
    log.info(f"request: {event_json_string}")
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "text/plain"},
        "body": f"You have hit {event_json_string}",
    }
