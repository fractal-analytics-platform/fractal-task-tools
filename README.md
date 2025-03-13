# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/fractal-analytics-platform/fractal-task-tools/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                                       |    Stmts |     Miss |   Branch |   BrPart |   Cover |   Missing |
|----------------------------------------------------------- | -------: | -------: | -------: | -------: | ------: | --------: |
| src/fractal\_task\_tools/\_\_init\_\_.py                   |        3 |        0 |        0 |        0 |    100% |           |
| src/fractal\_task\_tools/\_args\_schemas.py                |       83 |       13 |       30 |        7 |     79% |49-50, 59, 110->130, 133-135, 145->150, 162->173, 186-206 |
| src/fractal\_task\_tools/\_cli.py                          |       20 |       20 |        6 |        0 |      0% |      1-69 |
| src/fractal\_task\_tools/\_create\_manifest.py             |       88 |       88 |       26 |        0 |      0% |     4-196 |
| src/fractal\_task\_tools/\_descriptions.py                 |       81 |       32 |       34 |        9 |     56% |27, 52, 57, 62, 65, 71->75, 112->116, 138, 142-164, 182, 190, 217-236 |
| src/fractal\_task\_tools/\_package\_name\_tools.py         |        5 |        5 |        0 |        0 |      0% |      1-27 |
| src/fractal\_task\_tools/\_pydantic\_generatejsonschema.py |       18 |        0 |        4 |        1 |     95% |    27->32 |
| src/fractal\_task\_tools/\_signature\_constraints.py       |       38 |        9 |       16 |        6 |     69% |39, 44->49, 52-58, 77, 83, 87, 98 |
| src/fractal\_task\_tools/\_task\_docs.py                   |       47 |       47 |       16 |        0 |      0% |     1-109 |
| src/fractal\_task\_tools/\_titles.py                       |       37 |        5 |       22 |        8 |     78% |22->28, 31-33, 34->39, 65->70, 75->79, 83->81, 89-92, 95->100 |
| src/fractal\_task\_tools/task\_models.py                   |       58 |       58 |        0 |        0 |      0% |      1-94 |
|                                                  **TOTAL** |  **478** |  **277** |  **154** |   **31** | **41%** |           |


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