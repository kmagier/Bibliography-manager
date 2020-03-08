FROM python:3.7-alpine
WORKDIR /file_server
ENV FLASK_APP main.py
ENV FLASK_RUN_HOST 0.0.0.0
ENV FLASK_RUN_PORT 81
COPY ./file_server /file_server
RUN apk add --no-cache gcc musl-dev linux-headers openssl-dev libffi-dev postgresql-dev
RUN pip install -r requirements.txt
RUN pip install pyopenssl
CMD ["flask", "run", "--cert", "adhoc"]