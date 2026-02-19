# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/fractal-analytics-platform/fractal-task-tools/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                                 |    Stmts |     Miss |   Branch |   BrPart |   Cover |   Missing |
|----------------------------------------------------- | -------: | -------: | -------: | -------: | ------: | --------: |
| src/fractal\_task\_tools/\_\_init\_\_.py             |        3 |        0 |        0 |        0 |    100% |           |
| src/fractal\_task\_tools/\_args\_schemas.py          |       95 |        3 |       34 |        3 |     95% |56, 187->196, 216-217 |
| src/fractal\_task\_tools/\_cli.py                    |       27 |        8 |        8 |        1 |     63% |78, 84-100 |
| src/fractal\_task\_tools/\_cli\_tools.py             |       49 |        0 |        8 |        2 |     96% |85->94, 89->87 |
| src/fractal\_task\_tools/\_create\_manifest.py       |       67 |       13 |       26 |        7 |     76% |43, 68-70, 77-78, 87-89, 107->109, 110, 111->113, 114, 144-145, 149->153 |
| src/fractal\_task\_tools/\_deepdiff.py               |       50 |        0 |       22 |        0 |    100% |           |
| src/fractal\_task\_tools/\_descriptions.py           |       82 |        5 |       32 |        6 |     90% |27, 52, 57, 65, 232, 237->236 |
| src/fractal\_task\_tools/\_generatejsonschema.py     |       26 |        1 |       10 |        2 |     92% |39->42, 71 |
| src/fractal\_task\_tools/\_package\_name\_tools.py   |        5 |        0 |        0 |        0 |    100% |           |
| src/fractal\_task\_tools/\_signature\_constraints.py |       75 |        0 |       36 |        0 |    100% |           |
| src/fractal\_task\_tools/\_task\_arguments.py        |       26 |        0 |        6 |        0 |    100% |           |
| src/fractal\_task\_tools/\_task\_docs.py             |       47 |       15 |       16 |        4 |     63% |33->35, 35->37, 41-43, 91-107 |
| src/fractal\_task\_tools/\_titles.py                 |       37 |        3 |       22 |        2 |     92% |29-31, 80->78 |
| src/fractal\_task\_tools/\_union\_types.py           |       14 |        1 |        2 |        1 |     88% |        23 |
| src/fractal\_task\_tools/logging\_config.py          |       24 |        0 |        2 |        0 |    100% |           |
| src/fractal\_task\_tools/task\_models.py             |       99 |        4 |        0 |        0 |     96% |26, 30, 34, 38 |
| src/fractal\_task\_tools/task\_wrapper.py            |       37 |        0 |        8 |        1 |     98% |    76->85 |
| **TOTAL**                                            |  **763** |   **53** |  **232** |   **29** | **91%** |           |


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