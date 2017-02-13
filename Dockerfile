FROM alpine:3.5

ENV HOST "0.0.0.0"
ENV PORT "3535"


RUN apk update && \
    apk add python3 alpine-sdk python3-dev curl && \
    pip3 install PRCDNS && \
    apk del alpine-sdk python3-dev

ADD ./run.sh /
WORKDIR /

CMD ["sh", "-x", "/run.sh"]
