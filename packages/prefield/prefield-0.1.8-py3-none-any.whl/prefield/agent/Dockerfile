# latest prefect image for python 3.8
FROM prefecthq/prefect:latest-python3.9

WORKDIR /app

# Install required libraries
RUN pip install pip --upgrade
RUN pip install boto3

COPY start_agent.py /app
COPY __init__.py /app

ARG ENV=None
ARG aws_region=None
ARG AGENT_NAME=None
ENV PYTHONPATH=${PYTHONPATH}:${PWD} \
    ENV=$ENV \
    AGENT_NAME=$AGENT_NAME \
    PREFECT__LOGGING__EXTRA_LOGGERS="['prefield']"

ENTRYPOINT python3 /app/start_agent.py
