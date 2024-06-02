FROM python:3.10-slim-buster

WORKDIR /nugas

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY nugas/ .

EXPOSE 5000

ENTRYPOINT ["python"]

CMD ["manage.py", "runserver", "0.0.0.0:5000"]
