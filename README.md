#

<div align="center">

  <img src="assets/logo.png" alt="logo" width="400" height="auto" />
  <h1>WiseYoda</h1>

  <p>
    Quotes from the <a href="https://github.com/Mikaayenson/WiseYoda">Wise Yoda</a>
  </p>

<!-- Badges -->

[![Supported Python versions](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Python Testing](https://github.com/Mikaayenson/WiseYoda/actions/workflows/python-testing.yml/badge.svg)](https://github.com/Mikaayenson/WiseYoda/actions/workflows/python-testing.yml)

<h5>
    <a href="https://github.com/Mikaayenson/WiseYoda/issues/">Report Bug</a>
  <span> · </span>
    <a href="https://github.com/Mikaayenson/WiseYoda/issues/">Request Feature</a>
  </h5>
</div>

<br />

<!-- About the Project -->
## :star2: About the Project

Simple library to obtain wisdom from the wise Master Yoda in the form of quotes. Create a [feature request](https://github.com/Mikaayenson/WiseYoda/issues) if there are some useful features/commands that you hate to remember!

<!-- Screenshots -->
### :camera: Screenshots

<p align="center">
  <!-- <img width="969" alt="Terminal Output" src=""> -->
</p>

<!-- Getting Started -->
## :toolbox: Getting Started

<!-- Prerequisites -->
### :bangbang: Prerequisites

This project uses poetry as the python package manager

- `poetry` Follow the [poetry install](https://python-poetry.org/docs/) guide
- `python3.8+` Download from [python](https://www.python.org/downloads/) (ideally `3.10`)

```bash
   pip install wiseyoda
```

<!-- Usage -->
## :eyes: Usage

Reminder: These commands must be run in the virtualenv where you installed the dependencies.

```bash
  from wise_yoda import Quotes
  lesson = Quotes().random_quote()
  lesson = Quotes().select_quote(season=1, episode=1)
```

<!-- Run Locally -->
### :running: Run Locally

Clone the project

```bash
  git clone https://github.com/Mikaayenson/WiseYoda.git
```

Go to the project directory

```bash
  cd wise_yoda
```

Install system and Python dependencies

```bash
  make deps
```

Run wiseyoda

```bash
  wiseyoda --help
```

<!-- Development -->
### :construction: Development

<div align="center">
  <!-- <img width="969" alt="Make Help" src=""> -->
</div>

Install pre-commit

```bash
  pre-commit install
```

Update Python dependencies

```bash
  make deps-py-update
```

<!-- Running Tests -->
### :test_tube: Running Tests

Run tests

```bash
  make test
```

Run linter

```bash
  make check
```

<!-- Build: Poetry -->
### :triangular_flag_on_post: Build: Python Package

Build this project as a `sdist` and `wheel`

```bash
  make build
```


<!-- License -->
## :warning: License

Distributed under the Apache2.0 License. See LICENSE.txt for more information.
