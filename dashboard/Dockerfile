FROM python:3.12-slim
WORKDIR /app
COPY dashboard/app.py /app/app.py
COPY dashboard/static /app/static
EXPOSE 8080
CMD ["python", "/app/app.py"]
