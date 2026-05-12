FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
        iputils-ping \
        iproute2 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY stretch_head_control.py stretch_relay.py launcher.py \
     console_head_tracking.py head_tracking_3d.py \
     imu_server.py imu_viz.html ./

ENV PYTHONUNBUFFERED=1

CMD ["python3", "stretch_head_control.py"]
