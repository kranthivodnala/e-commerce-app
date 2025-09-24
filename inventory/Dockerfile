# Use slim python base
FROM python:3.11-slim

WORKDIR /app

# copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy app
COPY app.py .

ENV FLASK_ENV=production
ENV PORT=5000

# run with gunicorn for better behavior in containers
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app", "--workers", "1"]