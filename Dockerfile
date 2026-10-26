FROM python:3.13-slim
WORKDIR /app
RUN pip install --no-cache-dir fastapi==0.161.1 uvicorn==0.38.0
RUN useradd --create-home appuser
COPY src/lab_api.py /app/lab_api.py
USER appuser
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health',timeout=2)"
CMD ["uvicorn", "lab_api:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
