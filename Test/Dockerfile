FROM python:3.11-slim

WORKDIR /app

RUN pip install requests

COPY script.py .

CMD ["python", "-u", "script.py"]
