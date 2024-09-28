FROM spark:3.5.1-scala2.12-java17-python3-ubuntu

WORKDIR /app
USER root

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH="${PYTHONPATH}:/app"

RUN ln -sf $(which python3) /usr/bin/python && \
    ln -sf $(which pip3) /usr/bin/pip

RUN apt-get update
RUN apt-get install -y gcc python3-dev 
RUN pip install --upgrade pip setuptools

COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src /app/src
COPY ./main.py /app/main.py
COPY ./jars /jars

ENTRYPOINT [ "python", "main.py"]