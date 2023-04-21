FROM python:3.10.8-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN addgroup -S python && adduser -S python -G python
RUN pip install -U pipenv
USER python
WORKDIR /home/python
COPY --chown=python:python Pipfile Pipfile.lock ./
RUN pipenv install --system --deploy
COPY --chown=python:python /src .
COPY --chown=python:python /gunicorn/gunicorn.py .
ENV PATH="/home/python/.local/bin:${PATH}"
EXPOSE 8000
CMD ["gunicorn", "signal_documentation.wsgi:application", "-c", "gunicorn.py"]
