# agent

Functionality for running local and cloud agents.

## Deployment
* The docker image is built using the `docker_build` method under `cli.agent_commands.py`
  * The dockerfile and startup script are under `agent`
* `terraform` is then used to deploy the Fargate Service running the agent.
