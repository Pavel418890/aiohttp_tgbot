FROM python:3.10.3-slim-buster as builder

WORKDIR /app

RUN pip install --no-cache-dir -U pip install setuptools wheel

COPY requirements.txt ./

RUN \
    pip wheel \
    --no-cache-dir \
    --no-deps \
    --wheel-dir /app/wheels \
    -r requirements.txt

FROM python:3.10.3-slim-buster

COPY --from=builder /app/wheels /wheels

ENV HOME="/home/aiohttp-tgbot"
# ENV DATABASE_URL=
# ENV CLOUDAMQP=
# ENV MONGO_URL=
# ENV AWS_ACCESS_KEY=
# ENV AWS_SECRET_KEY=
# ENV AWS_REGION_NAME=
# ENV AWS_BUCKET_NAME=
# ENV BOT_TOKEN=

WORKDIR $HOME
RUN apt update && apt install -y gettext-base

RUN mkdir -p /home/aiohttp-tgbot && \
    addgroup --system --gid 1000 tgbot && \
    adduser --system --gid 1000 --uid 1000 tgbot

RUN pip install --no-cache-dir -U pip wheel setuptools && \
    pip install --no-cache  /wheels/*  && \
    find /usr/local/lib/python3.10/site-packages/ \
      -type d -name test -o -name tests \
      -o -type f -name "*.pyc" -o -name "*.pyo" \
      -exec rm -fr "{}" \;

COPY . .

RUN chown -R 1000:1000 . && chmod +x ./entrypoint.sh

USER tgbot

ENTRYPOINT "./entrypoint.sh"