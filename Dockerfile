FROM python:3.11-slim as base

RUN apt-get update
RUN apt-get install -y --no-install-recommends build-essential gcc

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements/base.txt requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt


FROM python:3.11-bullseye as test

WORKDIR /app

COPY --from=base /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY . /app

RUN pip install --no-cache-dir --upgrade -r /app/requirements/develop.txt

CMD ["sh", "-c", "coverage run -m pytest && coverage report -m"]

FROM python:3.11-bullseye as production

WORKDIR /app

COPY --from=base /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY app /app/app

CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80" ]
