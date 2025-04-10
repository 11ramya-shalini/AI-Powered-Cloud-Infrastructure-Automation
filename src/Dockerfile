FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install flask requests plotly
EXPOSE 5000
CMD ["python", "web_app/app.py"]