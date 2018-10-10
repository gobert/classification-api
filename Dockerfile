FROM python:3.7-alpine

# Set the working directory to /app
WORKDIR /app

# Update the distribution
RUN apk update

# Install dependencies
RUN apk add build-base postgresql-dev libpq

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies
RUN pip install -r requirements-dev.txt
RUN pip install -r requirements-common.txt

CMD ["pytest", "--", "tests.py"]
