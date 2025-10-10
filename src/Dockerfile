FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .  

RUN pip install -r requirements.txt --no-cache-dir

COPY . .

EXPOSE 8080

CMD [ "uvicorn", "test_api:app", "--host", "0.0.0.0", "--port", "8080" ]