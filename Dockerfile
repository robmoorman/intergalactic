FROM python:3.7
RUN mkdir -p /code
WORKDIR /code
COPY requirements.txt /code
RUN pip install -r /code/requirements.txt
COPY . /code
RUN pip install .
EXPOSE 5001
CMD intergalactic run
