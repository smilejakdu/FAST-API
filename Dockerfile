FROM ubuntu:latest
RUN apt-get update
RUN apt-get install -y python-dev python3-pip build-essential
WORKDIR /fast_api_watcha
COPY ["requirements.txt","."]
RUN pip install -r requirements.txt
COPY ["var.py","."]
CMD ["uvicorn", "main:app", "--reload"]
