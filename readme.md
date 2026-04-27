# ArrayEqual Evaluation Function

[![Request Production Deploy](https://img.shields.io/badge/Request-Production_Deploy-2ea44f?style=for-the-badge)](https://github.com/lambda-feedback/ArrayEqual/issues/new?template=release-request.yml)

Compares a student's response array against an answer array, checking whether all elements are within the supplied tolerances. Uses [numpy.allclose](https://numpy.org/doc/stable/reference/generated/numpy.allclose.html) under the hood, so arrays of any regular shape (1D, 2D, etc.) are supported.

## Table of Contents
- [ArrayEqual Evaluation Function](#arrayequal-evaluation-function)
  - [Table of Contents](#table-of-contents)
  - [Repository Structure](#repository-structure)
  - [Function Reference](#function-reference)
    - [Inputs](#inputs)
    - [Parameters](#parameters)
    - [Output](#output)
    - [Error handling](#error-handling)
    - [Examples](#examples)
  - [Development](#development)
    - [Running tests locally](#running-tests-locally)
  - [How it works](#how-it-works)
    - [Docker & Amazon Web Services (AWS)](#docker--amazon-web-services-aws)
    - [Middleware Functions](#middleware-functions)
    - [GitHub Actions](#github-actions)
  - [Pre-requisites](#pre-requisites)
  - [Contact](#contact)

## Repository Structure

```
app/
    __init__.py
    evaluation.py        # Main evaluation_function implementation
    evaluation_tests.py  # Unit tests for evaluation_function
    requirements.txt     # Python dependencies (numpy, evaluation-function-utils)
    Dockerfile           # Docker image definition for AWS Lambda
    docs/
        user.md          # User-facing documentation
        dev.md           # Developer notes

.github/
    workflows/
        test-lint.yml              # Lint and test on pull requests
        staging-deploy.yml         # Deploy to staging on push to main
        production-deploy.yml      # Manual production deployment
        pre_production_tests.yml   # Pre-production database validation tests

config.json   # Evaluation function name ("arrayEqual")
```

## Function Reference

### Inputs

| Field      | Type    | Description                              |
|------------|---------|------------------------------------------|
| `response` | array   | Student's submitted array                |
| `answer`   | array   | Correct answer array                     |
| `params`   | object  | Optional parameters (see below)          |

Both `response` and `answer` are parsed with `np.array(dtype=np.float32)`.

### Parameters

| Parameter                        | Type    | Default | Description                                                                 |
|----------------------------------|---------|---------|-----------------------------------------------------------------------------|
| `atol`                           | number  | `0`     | Absolute tolerance — maximum allowed absolute difference between elements   |
| `rtol`                           | number  | `0`     | Relative tolerance — maximum allowed relative difference between elements   |
| `feedback_for_incorrect_response`| string  | none    | If set, replaces the default feedback message for all incorrect responses   |

`atol` and `rtol` map directly to the corresponding parameters of `numpy.allclose`.

### Output

```json
{
  "is_correct": true
}
```

When the response is incorrect:

```json
{
  "is_correct": false,
  "feedback": "<message>"
}
```

### Error handling

- If `answer` contains non-numeric or empty values an exception is raised (the question is misconfigured).
- If `response` contains non-numeric values, `is_correct: false` is returned with the feedback `"Only numbers are permitted."`.
- If `response` contains empty fields, `is_correct: false` is returned with the feedback `"Response has at least one empty field."`.

### Examples

**Exact match (no tolerance)**

```json
{
  "response": [1, 2, 3],
  "answer":   [1, 2, 3],
  "params":   {}
}
```

```json
{ "is_correct": true }
```

**2D array with absolute tolerance**

```json
{
  "response": [[1, 2], [3, 4]],
  "answer":   [[1, 2], [3, 4.05]],
  "params":   { "atol": 0.1 }
}
```

```json
{ "is_correct": true }
```

**Custom feedback for incorrect response**

```json
{
  "response": [[1, 1], [1, 1]],
  "answer":   [[1, 1], [1, 0]],
  "params":   { "feedback_for_incorrect_response": "Check the last element of the second row." }
}
```

```json
{ "is_correct": false, "feedback": "Check the last element of the second row." }
```

## Development

### Running tests locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install pytest -r app/requirements.txt
pytest --tb=auto -v
```

## How it works

The function is built on top of a custom base layer, [BaseEvaluationFunctionLayer](https://github.com/lambda-feedback/BaseEvalutionFunctionLayer), which provides tooling, tests and schema checking common to all evaluation functions.

### Docker & Amazon Web Services (AWS)

The evaluation function runs on AWS Lambda inside a Docker container. Docker bundles the app and all its dependencies into a single image, giving full control over the Python version and packages used. For more information on Docker, read this [introduction to containerisation](https://www.freecodecamp.org/news/a-beginner-friendly-introduction-to-containers-vms-and-docker-79a9e3e119b/). To learn more about AWS Lambda, click [here](https://geekflare.com/aws-lambda-for-beginners/).

### Middleware Functions

Middleware provided by [BaseEvaluationFunctionLayer](https://github.com/lambda-feedback/BaseEvalutionFunctionLayer) handles request parsing, input validation and response formatting, so this repository only needs to implement the core comparison logic in `evaluation.py`.

### GitHub Actions

Three automated pipelines are configured under `.github/workflows/`:

- **`test-lint.yml`** — runs on every pull request; lints with flake8 and runs the unit test suite.
- **`staging-deploy.yml`** — runs on every push to `main`; builds the Docker image and deploys to the staging environment after tests pass.
- **`production-deploy.yml`** — manually triggered; runs database validation tests then promotes the image to production.

## Pre-requisites

To develop locally you will need:

- Python 3.8 or higher
- `git` CLI or GitHub Desktop
- A code editor (VS Code, PyCharm, etc.)
- Docker (optional — only needed to build/test the image locally)

## Contact

For questions or issues, open a GitHub issue or visit the [lambda-feedback organisation](https://github.com/lambda-feedback).