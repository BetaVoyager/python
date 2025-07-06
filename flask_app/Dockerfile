FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt && apt update && apt install -y curl
COPY . .
CMD ["sh", "-c", "gunicorn app:app --bind 0.0.0.0:5000"]
