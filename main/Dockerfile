FROM dockerhub.ir/python:3.8

COPY ./main.py / 

RUN pip3 install requests
RUN pip3 install redis
RUN pip3 install bs4
RUN pip3 install lxml 


CMD [ "python3", "./main.py" ]
