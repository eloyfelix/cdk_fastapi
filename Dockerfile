FROM mambaorg/micromamba:0.20.0

WORKDIR /code

COPY --chown=$MAMBA_USER:$MAMBA_USER environment.yaml /code/environment.yaml

RUN micromamba install -y -f /code/environment.yaml && \
    micromamba clean --all --yes

COPY ./app /code/app

RUN /opt/conda/bin/curl -Ls https://github.com/cdk/cdk/releases/download/cdk-2.7.1/cdk-2.7.1.jar -o /code/cdk.jar
RUN /opt/conda/bin/curl -Ls https://github.com/dan2097/opsin/releases/download/2.6.0/opsin-core-2.6.0-jar-with-dependencies.jar -o /code/opsin.jar

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]