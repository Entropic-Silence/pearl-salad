FROM ubuntu:22.04 AS download
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates curl && rm -rf /var/lib/apt/lists/*
WORKDIR /download
RUN curl -fL --retry 3 https://github.com/andru-kun/wildrig-multi/releases/download/0.51.2/wildrig-multi-linux-0.51.2.tar.gz -o miner.tar.gz \
 && echo 'da1463dcd3444687c7b29b1351e5bd2cb6b7fe204254f12cfac9796a17615c37  miner.tar.gz' | sha256sum -c - \
 && tar -xzf miner.tar.gz wildrig-multi readme.txt help.txt

FROM nvidia/cuda:12.8.1-runtime-ubuntu22.04
LABEL org.opencontainers.image.source="https://github.com/Entropic-Silence/pearl-salad"
LABEL org.opencontainers.image.description="Pearlhash WildRig GPU container for SaladCloud"
ENV NVIDIA_VISIBLE_DEVICES=all NVIDIA_DRIVER_CAPABILITIES=compute,utility PYTHONUNBUFFERED=1
RUN apt-get update && apt-get install -y --no-install-recommends python3 ca-certificates libnuma1 libcurl4 libssl3 libstdc++6 ocl-icd-libopencl1 \
 && rm -rf /var/lib/apt/lists/* \
 && mkdir -p /etc/OpenCL/vendors \
 && echo 'libnvidia-opencl.so.1' > /etc/OpenCL/vendors/nvidia.icd
WORKDIR /opt/miner
COPY --from=download /download/wildrig-multi /download/readme.txt /download/help.txt ./
COPY launcher.py ./
RUN chmod 755 wildrig-multi && ldd ./wildrig-multi > /tmp/ldd.txt && cat /tmp/ldd.txt && ! grep -q 'not found' /tmp/ldd.txt
ENTRYPOINT ["python3", "/opt/miner/launcher.py"]
