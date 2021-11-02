FROM dockerhub.ir/python:3.8

COPY save_rss_redis.py /
COPY rss_urls /

RUN pip3 install redis

CMD [ "python3", "./save_rss_redis.py" ]
