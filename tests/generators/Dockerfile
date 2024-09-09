FROM python:latest

WORKDIR /scripts/generators

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

RUN chmod +x fake-equipment.py

CMD ["python", "fake-equipment.py"]