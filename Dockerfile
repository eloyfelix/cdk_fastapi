FROM mambaorg/micromamba:0.19.1

WORKDIR /code

COPY --chown=$MAMBA_USER:$MAMBA_USER environment.yaml /code/environment.yaml

RUN micromamba install -y -f /code/environment.yaml && \
    micromamba clean --all --yes

COPY ./app /code/app

ARG MAMBA_DOCKERFILE_ACTIVATE=1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]