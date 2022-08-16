# syntax=docker/dockerfile:1
FROM python:3.10.6-slim-bullseye
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
#copy source code to workdir
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host=0.0.0.0"]

# to run this container:
# cd Service-Lowmaf/
# docker build -t service-lowmaf . 
# docker run -p 8000:8000 --name service-lowmaf service-lowmaf