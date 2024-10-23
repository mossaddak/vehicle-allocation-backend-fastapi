FROM python:3.12-alpine

# Install dependencies for MongoDB and required Python packages
RUN apk update && apk add gcc python3-dev musl-dev

# Set environment variable to ensure output is shown in real-time
ENV PYTHONBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

COPY requirements/development.txt requirements/development.txt
RUN pip install --no-cache-dir -r requirements/development.txt

COPY env_sample.txt .env

COPY . .

CMD ["uvicorn", "index:app", "--reload", "--host", "0.0.0.0", "--port", "5000"]
