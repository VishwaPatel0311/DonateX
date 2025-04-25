FROM python:3.9.1-slim-buster

# Setting work dir for docker to use
WORKDIR /usr/src/app

# Copy local requirements.txt to docker work dir
COPY app/requirements.txt /usr/src/app

RUN pip install --no-cache-dir -r requirements.txt

# Copy app in local storage to docker image
COPY app /usr/src/app

# Expose port
EXPOSE 14011

# Run app
CMD ["python", "main.py"]
