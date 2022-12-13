FROM python:3.10

RUN apt update; apt install -y cmake
COPY "requirements.txt" "/tmp/requirements.txt"
RUN pip install -r /tmp/requirements.txt

COPY "*.py" "/app/"

CMD ["python3", "ursabench.py"]
