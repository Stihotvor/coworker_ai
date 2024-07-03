# coworker_ai
## Description
This repository contains the code for the coworker-ai service. CoworkerAI is an AI assistant, which helps to track bugs,
features and whole projects using Jira tasks and company documentation.

## How to run PoC
In order to run the project locally You will need:
- LMStudio server running on `localhost:1234` with Your favourite model (I recommend Mistral one)
- Run `docker-compose up`
- Visit localhost:8010

## Directory structure
The code base is located in `src` directory. You can find there all the main domains of the project:
- UI
- API
- Role
- Storage

If You need to play with the system prompts, You can find them in `src/role/prompt_repository/system` directory.

## Tests
In order to run the tests, you need to connect to the coworker-ai service and type in the next command:
- for unit tests (marked as `unit` in the `pytest.ini` file)
```bash
poetry run pytest -m unit
```
- for integration tests (marked as `integration` in the `pytest.ini` file)
```bash
poetry run pytest -m integration
```
