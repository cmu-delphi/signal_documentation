FROM ubuntu:22.04

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
COPY Pipfile Pipfile.lock ./

RUN apt-get update -y
RUN apt-get install -y gcc default-libmysqlclient-dev pkg-config
RUN apt-get install mysql-client -y
RUN apt-get install graphviz graphviz-dev -y
RUN apt-get install python3 -y
RUN apt-get install python3-pip -y
RUN python3 -m pip install --upgrade pip
RUN pip3 install pipenv
RUN pipenv lock
RUN pipenv requirements > requirements.txt
RUN pip3 install -r requirements.txt

WORKDIR /home/python
COPY /src .
COPY /gunicorn/gunicorn.py .
ENV PATH="/home/python/.local/bin:${PATH}"
EXPOSE 8000
CMD ["gunicorn", "signal_documentation.wsgi:application", "-c", "gunicorn.py"]
