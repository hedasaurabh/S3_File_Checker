FROM python:3
WORKDIR /usr/src/app
COPY . .
RUN pip install boto3 pytz requests datetime
CMD ["python","./app.py"]
