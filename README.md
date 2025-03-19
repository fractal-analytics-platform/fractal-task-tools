# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/fractal-analytics-platform/fractal-task-tools/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                                       |    Stmts |     Miss |   Branch |   BrPart |   Cover |   Missing |
|----------------------------------------------------------- | -------: | -------: | -------: | -------: | ------: | --------: |
| src/fractal\_task\_tools/\_\_init\_\_.py                   |        3 |        0 |        0 |        0 |    100% |           |
| src/fractal\_task\_tools/\_args\_schemas.py                |       83 |        3 |       30 |        3 |     95% |59, 162->173, 193-194 |
| src/fractal\_task\_tools/\_cli.py                          |       26 |        8 |        8 |        1 |     62% | 70, 76-92 |
| src/fractal\_task\_tools/\_cli\_tools.py                   |       43 |       32 |        2 |        0 |     24% |25-41, 59-86 |
| src/fractal\_task\_tools/\_create\_manifest.py             |       60 |       13 |       24 |        8 |     73% |41, 68-70, 77-78, 83-85, 97->101, 102, 103->105, 106, 129-130, 134->138, 138->142 |
| src/fractal\_task\_tools/\_deepdiff.py                     |       27 |        0 |       22 |        0 |    100% |           |
| src/fractal\_task\_tools/\_descriptions.py                 |       81 |       11 |       34 |       10 |     82% |27, 52, 57, 65, 138, 150-151, 182, 190, 219, 224->223, 227 |
| src/fractal\_task\_tools/\_package\_name\_tools.py         |        5 |        0 |        0 |        0 |    100% |           |
| src/fractal\_task\_tools/\_pydantic\_generatejsonschema.py |       18 |        0 |        4 |        1 |     95% |    27->32 |
| src/fractal\_task\_tools/\_signature\_constraints.py       |       37 |        4 |       16 |        4 |     85% |76, 82, 86, 97 |
| src/fractal\_task\_tools/\_task\_docs.py                   |       47 |       15 |       16 |        4 |     63% |33->35, 35->37, 41-43, 91-109 |
| src/fractal\_task\_tools/\_titles.py                       |       37 |        3 |       22 |        2 |     92% |31-33, 83->81 |
| src/fractal\_task\_tools/task\_models.py                   |       57 |        0 |        0 |        0 |    100% |           |
| src/fractal\_task\_tools/task\_wrapper.py                  |       27 |        0 |        4 |        0 |    100% |           |
|                                                  **TOTAL** |  **551** |   **89** |  **182** |   **33** | **82%** |           |


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