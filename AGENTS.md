# AGENTS.md

This document provides essential knowledge for AI coding agents to be productive in the `selenium-wrapper` codebase. It outlines the architecture, workflows, conventions, and integration points specific to this project.

## Project Overview
`selenium-wrapper` is a Python package designed to simplify writing Selenium browser tests. It provides a pytest fixture (`browser`) for browser automation and includes utilities for common tasks like interacting with dropdowns, date pickers, and file downloads. Tests can be run locally or inside a Docker container.

### Key Components
- **`selenium_wrapper/`**: Core library for browser automation.
  - `browsers.py`: Provides a list of available browsers.
  - `locate_by.py`: Provides utilities for locating elements.
  - `selenium.py`: Core Selenium wrapper logic, including browser initialization.
  - `utils/`: Helper modules for date pickers, file paths, validation, etc.
- **`elements/`**: Page object models for specific websites.
- **`tests/`**: Contains test cases and pytest configurations.
  - `test_samples/`: Example tests demonstrating library usage.

### External Dependencies
- **Selenium**: For browser automation.
- **pytest**: For test execution.
- **Docker**: For running tests in isolated environments.

## Developer Workflows

### Setting Up the Environment
1. Clone the repository.
2. Create a virtual environment (Python 3.12+).
3. Install dependencies:
   - Using `uv`: `uv sync`
   - Using `pip`: `pip install -r requirements.txt`

### Running Tests
- **Locally**: Use `pytest` to run tests.
- **In Docker**:
  1. Ensure a `.env` file exists with the following variables:
     ```
     HEADLESS=True
     NUM_CORES=2
     ```
  2. Run: `docker compose up --build`

### Code Formatting and Linting
- Use `ruff format` and `ruff check` to ensure code style compliance.

### Debugging
- Use `pytest`'s `-s` flag to view print statements.
- Note: Tests cannot be run without headless mode in Docker.

## Project-Specific Conventions
- **Page Object Models**: Defined in `elements/`. Each file corresponds to a specific website.
- **Test Structure**: Example tests are in `tests/test_samples/`. Follow these patterns for new tests.
- **Environment Variables**: Use `.env` for configuration.
- **CI Checks**: Ensure test coverage remains above 80%.

## Integration Points
- **Docker**: Tests are designed to run in a Dockerized environment for consistency.
- **Media Examples**: GIFs in `media/examples/` demonstrate test behavior.

## Key Files and Directories
- `selenium_wrapper/`: Core library.
- `elements/`: Page object models.
- `tests/test_samples/`: Example tests.
- `Dockerfile` and `docker-compose.yml`: For Dockerized test execution.
- `README.md`: Usage instructions and examples.

## Notes for AI Agents
- Follow the patterns in `tests/test_samples/` for writing new tests.
- Use `selenium_wrapper/utils/` for common utilities.
- Refer to `README.md` for detailed usage examples.
- Ensure all new code passes `ruff` checks and maintains test coverage.

By adhering to these guidelines, AI agents can contribute effectively to the `selenium-wrapper` project.
