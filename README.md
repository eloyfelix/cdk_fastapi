# CDK FastAPI example

Quick and dirty [FastAPI](https://github.com/tiangolo/fastapi) API to play a bit with [CDK](https://github.com/cdk/cdk) and [OPSIN](https://github.com/dan2097/opsin)

- Clone the repo and build the image.

  ```
  git clone https://github.com/eloyfelix/cdk_fastapi.git
  cd cdk_fastapi
  docker build -t cdk_fastapi .
  ```

- Run the container using the image.

  ```
  docker run -p8000:8000 cdk_fastapi
  ```

- Open FastAPI docs:

  http://localhost:8000/docs
