# Project Guidelines

## Code Style
- Every Python file MUST start with a top-level docstring comment explaining its module-level purpose at the very top.
- The project strictly abides by `pylint`. When functions or classes throw linting errors that are intentional, use inline disable comments (e.g., `# pylint: disable=too-few-public-methods` in ORMs and `# pylint: disable=unused-argument` in test setups/fastapi contexts).

## Architecture
- The application uses FastAPI with an MVC-like layered architecture:
  - **Controllers** (`app/controllers/`): Define FastAPI routers to handle HTTP requests/responses.
  - **Services** (`app/services/`): Contain the core business logic.
  - **Models** (`app/models.py`): SQLAlchemy ORM models.
  - **Schemas** (`app/schemas.py`): Pydantic models for request validation.
- Initial data loading relies on reading from a CSV (`users.csv`) into in-memory storage during startup (`app/database.py`).

## Build and Test
- **Run Application**: `docker-compose up --build -d`
- **API Endpoints**: Local server at `http://localhost:8000` with Swagger UI at `http://localhost:8000/docs`
- **Testing**: Run tests using `pytest tests/`. 
- **Mocking Strategy**: Pytest files (e.g., `tests/test_menu.py`) depend on FastAPI's `TestClient` and implement `setup_module()` and `teardown_module()` to initialize and clean up dummy memory datastores.

## Conventions
- Refer to `README.md` for complete API documentation, database interaction status, and basic gotchas.
