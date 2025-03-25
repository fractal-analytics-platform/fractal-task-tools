# Contribute to Fractal Task Tools development

```console
$ python -m venv venv

$ source venv/bin/activate

$ python -m pip install -e .[dev,docs]
[...]

$ pre-commit install
pre-commit installed at .git/hooks/pre-commit
```

## How to make a release
From the development environment:
```
bumpver update --patch --dry
```

## Tests

Run e.g. one of these commands
```
pytest
pytest -s -vvv --log-cli-level info --full-trace
```

## Documentation

The documentation is built with mkdocs, and we bundle a module from
[sphinx-argparse plugin](https://sphinx-argparse.readthedocs.io), customized to
our needs.

To build or server the documentation locally run
```
mkdocs serve --config-file mkdocs.yml  # serves the docs at http://127.0.0.1:8000

mkdocs build --config-file mkdocs.yml  # creates a build in the `site` folder
```
