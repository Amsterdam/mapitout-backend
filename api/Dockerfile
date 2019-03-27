FROM amsterdam/python
    ENV PYTHONUNBUFFERED 1
    RUN mkdir -p /static && chown datapunt /static
    RUN mkdir -p /app && chown -R datapunt /app
    RUN mkdir -p /deploy && chown -R datapunt /deploy

    COPY src /app/
    COPY deploy /deploy/
    COPY requirements.txt /app/
    WORKDIR /app
    RUN pip install -r requirements.txt
    USER datapunt
    CMD uwsgi -s /tmp/mapitout.sock --manage-script-name --mount /=proxy_server:app