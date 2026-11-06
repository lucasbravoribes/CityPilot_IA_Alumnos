FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /workspace
RUN pip install --no-cache-dir jupyterlab ipykernel requests pandas SQLAlchemy 'psycopg[binary]>=3.2,<4' matplotlib pytest
EXPOSE 8888
