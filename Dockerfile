FROM python:2

RUN pip install streamlink

WORKDIR /app
ADD roku-hls.py roku-hls.py
CMD python roku-hls.py
