FROM python:3.11-alpine

# set a directory for the app
WORKDIR /fileserver

RUN pip install --upgrade pip

COPY ./pyproject.toml .
RUN pip install ".[dev]"

COPY . .

EXPOSE 80

ENTRYPOINT ["gunicorn", "-b", ":80", "app:create_app()"]
