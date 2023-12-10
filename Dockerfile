FROM public.ecr.aws/lambda/python:3.11

# Install poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python \
    && cd /usr/local/bin \
    && ln -s /opt/poetry/bin/poetry \
    && poetry config virtualenvs.create false

## Getting Large models
# Getting Pose Landmark model https://developers.google.com/mediapipe/solutions/vision/pose_landmarker#get_started
RUN curl -LO https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_heavy/float16/latest/pose_landmarker_heavy.task
# Getting Object Detection model https://developers.google.com/mediapipe/solutions/vision/object_detector
RUN curl -LO https://storage.googleapis.com/mediapipe-models/object_detector/efficientdet_lite0/float16/latest/efficientdet_lite0.tflit

COPY src/ ${LAMBDA_TASK_ROOT}
COPY pyproject.toml poetry.lock ${LAMBDA_TASK_ROOT}
# Install python packages
RUN poetry install --no-root

# CMD [ "resize.handler" ]