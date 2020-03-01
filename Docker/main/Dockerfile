FROM python:3.7-alpine
WORKDIR /app
ENV FLASK_APP app.py
ENV FLASK_RUN_HOST 0.0.0.0
ENV FLASK_RUN_PORT 80
COPY ./app /app
RUN apk add --no-cache gcc musl-dev linux-headers openssl-dev libffi-dev postgresql-dev
RUN pip install -r requirements.txt
RUN pip install pyopenssl
CMD ["flask", "run", "--cert", "adhoc"]