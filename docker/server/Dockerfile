FROM python:3.9.9
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

ARG GID=1000
ARG UID=1000
ARG USER=ubuntu

RUN apt-get update && \
    apt-get install gettext -y && \
    groupadd -g $GID $USER && \
    useradd  -u $UID -g $GID $USER

WORKDIR /app

COPY src/requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt --no-cache-dir

COPY ./src /app

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host=0.0.0.0" , "--reload" , "--port", "8000"]

USER $USER