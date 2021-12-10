FROM python:latest
WORKDIR /usr/app/src
COPY test.py ./
RUN pip install neo4j
CMD [ "python", "./test.py"]