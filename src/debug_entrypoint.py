from resize import handler

bucket_name = "testbucket-for-opencv-irodolly"
key = "target/i56.jpg"

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
