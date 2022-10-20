FROM mambaorg/micromamba:0.20.0

WORKDIR /code

COPY --chown=$MAMBA_USER:$MAMBA_USER environment.yaml /code/environment.yaml

RUN micromamba install -y -f /code/environment.yaml && \
    micromamba clean --all --yes

RUN /opt/conda/bin/curl -Ls https://github.com/cdk/cdk/releases/download/cdk-2.8/cdk-2.8.jar -o /code/cdk.jar
RUN /opt/conda/bin/curl -Ls https://github.com/dan2097/opsin/releases/download/2.7.0/opsin-core-2.7.0-jar-with-dependencies.jar -o /code/opsin.jar
# from https://gitlab.com/glycoinfo/molwurcs
COPY MolWURCS.jar /code/MolWURCS.jar

COPY ./app /code/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]