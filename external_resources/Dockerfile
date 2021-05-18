FROM python:3.8

WORKDIR /app/external_resources
ADD . /app/external_resources
RUN pip install -r requirements.txt
ENV PYTHONPATH "${PYTHONPATH}:/app/external_resources"
ENTRYPOINT ["python", "app.py"]
