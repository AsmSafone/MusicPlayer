FROM python:3.10

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3", "GuYsMETI/main.py"]
