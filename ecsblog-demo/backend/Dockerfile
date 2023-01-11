FROM python:3.12.0a4-alpine3.17

WORKDIR /app 
COPY requirements.txt /app
RUN pip3 install -r requirements.txt 
COPY main.py /app/main.py 
ENTRYPOINT ["python3"] 
CMD ["/app/main.py"]
