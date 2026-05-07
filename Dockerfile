FROM python:3.11

WORKDIR /app

COPY . .

RUN pip install requests pandas

CMD sh -c "python app/main.py && python app/import_data.py && python app/analyse.py"