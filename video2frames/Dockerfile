FROM python:3.7.10-slim-buster
WORKDIR /app
COPY requirements.txt requirements.txt
COPY . .
RUN pip3 install -r requirements.txt

CMD ["python3", "app.py"]
