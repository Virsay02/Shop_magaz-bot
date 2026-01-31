FROM python:3-11 slim

WORKDIR /app

COPY requiremnets.txt

RUN pip install --no-cache-dir -r requiremnets.txt

COPY . .

CMD ["python","run.py"]