FROM python:3.10-slim-buster

WORKDIR /nayla

COPY requirement.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirement.txt

COPY nayla/ .

EXPOSE 5000

ENTRYPOINT ["python"]

CMD ["manage.py","runserver","0.0.0.0:5000"]