FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
RUN useradd --create-home --uid 10001 app
WORKDIR /app
RUN pip install --no-cache-dir "fastapi>=0.110" "pydantic>=2.5" "uvicorn>=0.29" "pyjwt>=2.8" "argon2-cffi>=23.1"
COPY src ./src
USER app
EXPOSE 8000
CMD ["uvicorn", "main:app", "--app-dir", "src", "--host", "0.0.0.0", "--port", "8000"]