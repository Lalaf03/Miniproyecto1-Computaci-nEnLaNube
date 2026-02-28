FROM python:3.10-slim

WORKDIR /app

# 🔧 Dependencias necesarias para mysqlclient
RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . . 

EXPOSE 5001

CMD ["python", "run.py"]
