FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ .
EXPOSE 5000
CMD ["gunicorn", "-b", "0.0.0.0:5000", "web_app.app:app"]
