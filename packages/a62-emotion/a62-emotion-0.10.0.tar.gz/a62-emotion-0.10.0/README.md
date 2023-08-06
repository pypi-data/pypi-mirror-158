# Emotion

A model for emotion classification based on text and audio.

[![emotion - merge](https://github.com/philipGaudreau/emotion/actions/workflows/merge.yml/badge.svg)](https://github.com/philipGaudreau/emotion/actions/workflows/merge.yml)
[![emotion - pr](https://github.com/philipGaudreau/emotion/actions/workflows/pr.yml/badge.svg?event=pull_request)](https://github.com/philipGaudreau/emotion/actions/workflows/pr.yml)
[![emotion - push](https://github.com/philipGaudreau/emotion/actions/workflows/push.yml/badge.svg?event=push)](https://github.com/philipGaudreau/emotion/actions/workflows/push.yml)
[![MIT License](https://img.shields.io/apm/l/atomic-design-ui.svg?)](https://github.com/tterb/atomic-design-ui/blob/master/LICENSEs)

## Acknowledgements

 - Hafed Benteftifa
 - Soumaya Chaffar

## Features

Give audio and text as input and get back the dominant emotion.

## Usage/Examples

```python
[TODO]
```

## API Reference [TODO]

#### Get all items

```http
  GET /api/items
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `api_key` | `string` | **Required**. API key      |

#### Get item

```http
  GET /api/items/${id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. Id of item to fetch |

## Installation

Install emotion with pip

```bash
  pip install emotion
```

## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`GDRIVE_CREDENTIALS_DATA`

`SECRET_KEY`

## Run Locally

Be sure to have python 3.8 as the python executable
```bash
python3 --version
```

To install Poetry, run:
```bash
curl -sSL https://install.python-poetry.org | POETRY_VERSION=1.2.0b1 python3 - --yes
```

Clone the project

```bash
git clone https://github.com/philipgaudreau/emotion
```

Go to the project directory

```bash
cd emotion
```

Install dependencies (add flag `--default` if you do not want development dependencies)

```bash
poetry install
```

Activate the virtual environment

```bash
poetry shell
```

Start using the command line interface

```bash
emotion --help
```

## Running Tests

To run tests, run the following command (development dependencies must be installed)

```bash
pytest tests
```

## Deployment

To deploy this project run

```bash
[TODO]
```

## Tech Stack

**Client:** flask, [TODO]

**Server:** python,  [TODO]
## Feedback

If you have any feedback, please reach out to one of us.


## Authors

- [@philipgaudreau](https://github.com/philipgaudreau)
- [@guraymo](https://github.com/guraymo)
- [@gtrottier](https://github.com/gtrottier)


## 🚀 About Us
We are on our way to finish a degree in Machine Learning.


## License

[MIT](https://choosealicense.com/licenses/mit/)

