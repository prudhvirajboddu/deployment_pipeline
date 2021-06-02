ARG UBUNTU_VERSION=18.04

FROM ubuntu:${UBUNTU_VERSION} as base

RUN apt-get update && apt-get install -y curl

# See http://bugs.python.org/issue19846
ENV LANG C.UTF-8

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip

RUN python3 -m pip --no-cache-dir install --upgrade \
    "pip<20.3" \
    setuptools

# Some TF tools expect a "python" binary
RUN ln -s $(which python3) /usr/local/bin/python

ENV PYTHONUNBUFFERED True

# Copy local code to the container image.
WORKDIR /app

RUN curl https://storage.googleapis.com/models_melanoma/model.tflite --output "model.tflite"

COPY . .

RUN pip3 install -r requirements.txt

RUN mkdir uploads

CMD ["python","app.py"]