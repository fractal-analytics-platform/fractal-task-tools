# Contribute to Fractal Task Tools development


## Setup environment

We use [uv](https://docs.astral.sh/uv/) to manage the development environment and the dependencies - see https://docs.astral.sh/uv/getting-started/installation/ for methods to install it.
From the `fractal-task-tools` root folder, you can get started through
```bash
# Create a new virtual environment in `.venv`
uv venv

# Install both the required dependencies and the optional dev/docs dependencies
uv sync --all-extras
```

## Set up `pre-commit`

We use [pre-commit](https://pre-commit.com) to run [several checks](https://github.com/fractal-analytics-platform/fractal-task-tools/blob/main/.pre-commit-config.yaml) on files that are being committed. To set it up locally, you should run
```bash
# Install pre-commit globally (e.g. via `pipx`)
pipx install pre-commit

# Add the pre-commit hook to your local repository
pre-commit install
```

## Make a release

```
uv run --frozen bumpver update --patch --dry
```

## Tests

Run e.g. one of these commands
```
uv run --frozen pytest
uv run --frozen pytest -s -vvv --log-cli-level info --full-trace
```

## Documentation

The documentation is built with `mkdocs`, and we bundle a module from
[sphinx-argparse plugin](https://sphinx-argparse.readthedocs.io), customized to
our needs.

To build or server the documentation locally run
```
uv run --frozen mkdocs serve --config-file mkdocs.yml  # serves the docs at http://127.0.0.1:8000

uv run --frozen mkdocs build --config-file mkdocs.yml  # creates a build in the `site` folder
```
