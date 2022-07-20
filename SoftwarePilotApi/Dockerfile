FROM python:3.8

WORKDIR /cv-app

RUN apt-get update

RUN apt install -y libgl1-mesa-glx

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./app ./app

CMD ["python", "./app/cvApi.py"]
