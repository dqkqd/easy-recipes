FROM python:3.11

# set a directory for the app
WORKDIR /backend

COPY ./pyproject.toml .

RUN pip install --upgrade pip
RUN pip install ".[dev]"

COPY . .

EXPOSE 8080

CMD ["gunicorn", "-b", ":8080", "app:create_app()"]
