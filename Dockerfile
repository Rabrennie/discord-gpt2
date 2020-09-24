FROM tensorflow/tensorflow:1.15.0-py3

ENV LANG=C.UTF-8

RUN mkdir /gpt-2
WORKDIR /gpt-2
ADD . /gpt-2

RUN pip install --upgrade pip
RUN pip3 install -r requirements.txt
RUN pip3 install discord
RUN pip3 install flask

CMD ["python3", "./server.py"]