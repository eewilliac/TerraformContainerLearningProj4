FROM ubuntu:latest
RUN apt-get update && apt-get install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get update && apt-get install -y python3.12 python3.12-dev
RUN apt-get update && apt-get install -y python3-pip
RUN apt install -y python3-pip
#COPY . .
COPY requirements.txt .
COPY ./templates ./templates
COPY app.py .
RUN pip install -r requirements.txt --break-system-packages --ignore-installed

EXPOSE 5000
CMD ["python3", "app.py"]