FROM ubuntu:latest
RUN apt-get update
RUN apt-get install -y python3-dev python3-pip build-essential
WORKDIR /fast_backend
COPY ["requirements.txt","."]
RUN pip install -r requirements.txt
CMD ["uvicorn", "main:app", "--reload","--port","13013"]
