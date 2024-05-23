FROM python:3.9

WORKDIR /code

# Install netcat for wait-for-it script
RUN apt-get update && apt-get install -y netcat-openbsd

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app
COPY ./wait-for-it.sh /code/wait-for-it.sh
RUN chmod +x /code/wait-for-it.sh

EXPOSE 8000

CMD ["/code/wait-for-it.sh", "microservices-demo-name-mysql", "--", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
