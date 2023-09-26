FROM python:3.11-alpine

# set a directory for the app
WORKDIR /backend

RUN pip install --upgrade pip
COPY ./pyproject.toml .
RUN pip install .

COPY . .

EXPOSE 8080
ENTRYPOINT ["gunicorn", "-b", ":8080", "app:create_app()"]
