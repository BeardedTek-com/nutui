FROM ghcr.io/home-assistant/amd64-base-python:3.10-alpine3.15
RUN apk --no-cache add \
        py3-pip pcre pcre2 nano \
        python3-dev build-base linux-headers pcre-dev
RUN mkdir /nutui
WORKDIR /nutui
RUN python3 -m venv venv
COPY requirements.txt /nutui
RUN source venv/bin/activate && \
    pip install wheel && \
    pip install -r requirements.txt
COPY nutui.py /nutui
COPY uwsgi.py /nutui
COPY uwsgi.ini /nutui
COPY app /nutui/app
COPY rootfs /
RUN chown -R 1000:1000 /nutui
EXPOSE 5000