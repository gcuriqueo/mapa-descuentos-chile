FROM python:3.7-alpine
WORKDIR /app
COPY ./app /app
COPY requirements.txt .
RUN pip install -r requirements.txt
EXPOSE 8100
CMD ["python", "/app/main.py"]