# Fractal task tools

[![PyPI version](https://img.shields.io/pypi/v/fractal-task-tools?color=gree)](https://pypi.org/project/fractal-task-tools/)
[![License](https://img.shields.io/badge/License-BSD_3--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)
[![CI Status](https://github.com/fractal-analytics-platform/fractal-task-tools/actions/workflows/ci.yml/badge.svg)](https://github.com/fractal-analytics-platform/fractal-task-tools/actions/workflows/ci_pip.yml)
[![Coverage](https://raw.githubusercontent.com/fractal-analytics-platform/fractal-task-tools/python-coverage-comment-action-data/badge.svg)](https://htmlpreview.github.io/?https://github.com/fractal-analytics-platform/fractal-task-tools/blob/python-coverage-comment-action-data/htmlcov/index.html)

Fractal-task-tools provides some basic tools for building tasks for the [Fractal](https://fractal-analytics-platform.github.io/) framework.

![Fractal_overview_small](https://github.com/user-attachments/assets/666c8797-2594-4b8e-b1d2-b43fca66d1df)

[Fractal](https://fractal-analytics-platform.github.io/) is a framework developed at the [BioVisionCenter](https://www.biovisioncenter.uzh.ch/en.html) to process bioimaging data at scale in the OME-Zarr format and prepare the images for interactive visualization.


# Get started
```console
$ python -m venv venv

$ source venv/bin/activate

$ python -m pip install -e .
[...]
Successfully installed annotated-types-0.7.0 docstring-parser-0.15 fractal-task-tools-0.0.1 pydantic-2.8.2 pydantic-core-2.20.1 typing-extensions-4.12.2

$ fractal-manifest create --help
usage: fractal-manifest create [-h] --package PACKAGE [--task-list-path TASK_LIST_PATH]

Create new manifest file

options:
  -h, --help            show this help message and exit
  --package PACKAGE     Example: 'fractal_tasks_core'
  --task-list-path TASK_LIST_PATH
                        Dot-separated path to the `task_list.py` module, relative to the package root (default value:
                        'dev.task_list').

```

# Development

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


## Contributors and license

Fractal was conceived in the Liberali Lab at the Friedrich Miescher Institute for Biomedical Research and in the Pelkmans Lab at the University of Zurich by [@jluethi](https://github.com/jluethi) and [@gusqgm](https://github.com/gusqgm). The Fractal project is now developed at the [BioVisionCenter](https://www.biovisioncenter.uzh.ch/en.html) at the University of Zurich and the project lead is with [@jluethi](https://github.com/jluethi). The core development is done under contract by [eXact lab S.r.l.](https://www.exact-lab.it).

Unless otherwise specified, Fractal components are released under the BSD 3-Clause License, and copyright is with the BioVisionCenter at the University of Zurich.
