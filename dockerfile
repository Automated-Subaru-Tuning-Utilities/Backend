# syntax=docker/dockerfile:1
FROM python:3.10.6-alpine
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
#copy source code to workdir
COPY . .
CMD ["uvicorn", "main:app"]
