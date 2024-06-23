FROM python:3.12-slim
LABEL authors="Yevhen Dyachenko"

# Install curl and poetry
RUN apt-get update &&  \
    apt-get install -y curl  \
    && apt-get clean \
    && pip install poetry

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies using poetry
RUN poetry config virtualenvs.create false \
  && poetry install --no-dev

# Set the working directory to /app/src
WORKDIR /app

ENTRYPOINT ["uvicorn", "src.main:app", "--reload", "--host", "0.0.0.0", "--port", "8010"]