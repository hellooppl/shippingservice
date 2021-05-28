FROM python:3.8
ENV PYTHONUNBUFFERED=1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
RUN chmod 777 entrypoint.sh
COPY . /code/
ENTRYPOINT /code/entrypoint.sh