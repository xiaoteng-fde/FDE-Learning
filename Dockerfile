FROM python:3.11-slim
WORKDIR /app
COPY day03.py .
CMD ["python","day03.py"]