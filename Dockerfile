FROM locustio/locust

USER $USERNAME

# Use non-root user as a security measure
#RUN groupadd -g 61000 docker
#RUN useradd -g 61000 -l -m -s /bin/false -u 61000 docker

# Setup and install poetry
RUN apt update && \
    apt install -y git curl && \
    pip install poetry

# cacheing project requirements
WORKDIR /code

#COPY poetry.lock pyproject.toml /code/
COPY pyproject.toml /code/
COPY poetry.lock pyproject.toml /code/

# installing project requirements
RUN poetry install --no-interaction --no-ansi --no-root

COPY . /code

ENTRYPOINT [ "poetry", "run", "locust" ]