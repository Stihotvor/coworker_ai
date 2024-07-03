# coworker_ai

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
