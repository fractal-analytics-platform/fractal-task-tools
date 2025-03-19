# Contribute to Fractal Task Tools development

```console
$ python -m venv venv

$ source venv/bin/activate

$ python -m pip install -e .[dev]
[...]
Successfully installed asttokens-2.4.1 bumpver-2024.1130 click-8.1.8 colorama-0.4.6 coverage-7.6.12 devtools-0.12.2 exceptiongroup-1.2.2 executing-2.2.0 fractal-task-tools-0.0.1 iniconfig-2.0.0 lexid-2021.1006 packaging-24.2 pluggy-1.5.0 pygments-2.19.1 pytest-8.3.5 six-1.17.0 toml-0.10.2 tomli-2.2.1

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
