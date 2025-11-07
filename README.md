# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/fractal-analytics-platform/fractal-task-tools/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                                       |    Stmts |     Miss |   Branch |   BrPart |   Cover |   Missing |
|----------------------------------------------------------- | -------: | -------: | -------: | -------: | ------: | --------: |
| src/fractal\_task\_tools/\_\_init\_\_.py                   |        3 |        0 |        0 |        0 |    100% |           |
| src/fractal\_task\_tools/\_args\_schemas.py                |       94 |        3 |       34 |        3 |     95% |57, 185->196, 216-217 |
| src/fractal\_task\_tools/\_cli.py                          |       26 |        8 |        8 |        1 |     62% | 71, 77-93 |
| src/fractal\_task\_tools/\_cli\_tools.py                   |       43 |        0 |        2 |        0 |    100% |           |
| src/fractal\_task\_tools/\_create\_manifest.py             |       67 |       13 |       26 |        7 |     76% |42, 69-71, 78-79, 90-92, 110->114, 115, 116->118, 119, 149-150, 154->158 |
| src/fractal\_task\_tools/\_deepdiff.py                     |       27 |        0 |       22 |        0 |    100% |           |
| src/fractal\_task\_tools/\_descriptions.py                 |       84 |        8 |       34 |        9 |     86% |27, 52, 57, 65, 198, 206, 235, 240->239, 243 |
| src/fractal\_task\_tools/\_package\_name\_tools.py         |        5 |        0 |        0 |        0 |    100% |           |
| src/fractal\_task\_tools/\_pydantic\_generatejsonschema.py |       18 |        0 |        4 |        1 |     95% |    27->32 |
| src/fractal\_task\_tools/\_signature\_constraints.py       |       40 |        0 |       18 |        0 |    100% |           |
| src/fractal\_task\_tools/\_task\_arguments.py              |       26 |        0 |        6 |        0 |    100% |           |
| src/fractal\_task\_tools/\_task\_docs.py                   |       47 |       15 |       16 |        4 |     63% |33->35, 35->37, 41-43, 91-109 |
| src/fractal\_task\_tools/\_titles.py                       |       37 |        3 |       22 |        2 |     92% |31-33, 83->81 |
| src/fractal\_task\_tools/\_union\_types.py                 |       12 |        2 |        4 |        2 |     75% |     8, 28 |
| src/fractal\_task\_tools/task\_models.py                   |       99 |        4 |        0 |        0 |     96% |26, 30, 34, 38 |
| src/fractal\_task\_tools/task\_wrapper.py                  |       27 |        0 |        4 |        0 |    100% |           |
|                                                  **TOTAL** |  **655** |   **56** |  **200** |   **29** | **89%** |           |


## Setup coverage badge

Below are examples of the badges you can use in your main branch `README` file.

### Direct image

[![Coverage badge](https://raw.githubusercontent.com/fractal-analytics-platform/fractal-task-tools/python-coverage-comment-action-data/badge.svg)](https://htmlpreview.github.io/?https://github.com/fractal-analytics-platform/fractal-task-tools/blob/python-coverage-comment-action-data/htmlcov/index.html)

This is the one to use if your repository is private or if you don't want to customize anything.

### [Shields.io](https://shields.io) Json Endpoint

[![Coverage badge](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/fractal-analytics-platform/fractal-task-tools/python-coverage-comment-action-data/endpoint.json)](https://htmlpreview.github.io/?https://github.com/fractal-analytics-platform/fractal-task-tools/blob/python-coverage-comment-action-data/htmlcov/index.html)

Using this one will allow you to [customize](https://shields.io/endpoint) the look of your badge.
It won't work with private repositories. It won't be refreshed more than once per five minutes.

### [Shields.io](https://shields.io) Dynamic Badge

[![Coverage badge](https://img.shields.io/badge/dynamic/json?color=brightgreen&label=coverage&query=%24.message&url=https%3A%2F%2Fraw.githubusercontent.com%2Ffractal-analytics-platform%2Ffractal-task-tools%2Fpython-coverage-comment-action-data%2Fendpoint.json)](https://htmlpreview.github.io/?https://github.com/fractal-analytics-platform/fractal-task-tools/blob/python-coverage-comment-action-data/htmlcov/index.html)

This one will always be the same color. It won't work for private repos. I'm not even sure why we included it.

## What is that?

This branch is part of the
[python-coverage-comment-action](https://github.com/marketplace/actions/python-coverage-comment)
GitHub Action. All the files in this branch are automatically generated and may be
overwritten at any moment.