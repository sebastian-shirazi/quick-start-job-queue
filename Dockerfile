FROM python:3.12-slim

WORKDIR /app

VOLUME [ "/app" ]

COPY poetry.lock pyproject.toml ./

RUN pip3 install --upgrade pip
RUN pip3 install poetry

COPY ./requirements.txt ./
RUN pip install -r requirements.txt

CMD ["flask", "--app", "application", "--debug", "run", "--host=0.0.0.0"]