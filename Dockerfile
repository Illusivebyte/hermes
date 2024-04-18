FROM python:3.13.0a4-slim
WORKDIR /app
COPY ./dist/hermes-0.0.1-py2.py3-none-any.whl .
RUN pip install ./hermes-0.0.1-py2.py3-none-any.whl
EXPOSE 8080
ENTRYPOINT [ "hermes" ]