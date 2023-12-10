from pose_detection import handler

bucket_name = "testbucket-for-opencv-irodolly"
key = "i56.jpg"

if __name__ == "__main__":
    handler(
        {
            "Records": [
                {
                    "s3": {
                        "bucket": {"name": bucket_name},
                        "object": {"key": key},
                    },
                },
            ],
        },
        {},
    )
