FROM python:3.11

WORKDIR /app

COPY main.py .

CMD ["python", "app/main.py"]