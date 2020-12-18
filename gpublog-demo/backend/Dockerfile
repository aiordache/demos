FROM tensorflow/tensorflow:latest-gpu

WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/

EXPOSE 5000

CMD python server.py
