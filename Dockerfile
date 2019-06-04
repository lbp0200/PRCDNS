FROM alpine:3.9

ENV HOST "0.0.0.0"
ENV PORT "3535"


RUN apk update && \
    apk add python3 alpine-sdk python3-dev libffi-dev curl && \
    pip3 install 'aiohttp<3.0' PRCDNS && \
    apk del alpine-sdk python3-dev libffi-dev

ADD ./run.sh /
WORKDIR /

CMD ["sh", "-x", "/run.sh"]
