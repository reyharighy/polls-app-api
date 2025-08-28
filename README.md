<div id="top">

<!-- HEADER STYLE: CLASSIC -->
<div align="center">

<img src="polls-app-api.png" width="30%" style="position: relative; top: 0; right: 0;" alt="Project Logo"/>

# POLLS-APP-API

<em>A simple polling application using FastAPI</em>

<!-- BADGES -->
<img src="https://img.shields.io/github/last-commit/reyharighy/polls-app-api?style=flat&logo=git&logoColor=white&color=0080ff" alt="last-commit">
<img src="https://img.shields.io/github/languages/top/reyharighy/polls-app-api?style=flat&color=0080ff" alt="repo-top-language">
<img src="https://img.shields.io/github/languages/count/reyharighy/polls-app-api?style=flat&color=0080ff" alt="repo-language-count">

<em>Built with the tools and technologies:</em>

<img src="https://img.shields.io/badge/Redis-FF4438.svg?style=flat&logo=Redis&logoColor=white" alt="Redis">
<img src="https://img.shields.io/badge/FastAPI-009688.svg?style=flat&logo=FastAPI&logoColor=white" alt="FastAPI">
<img src="https://img.shields.io/badge/Python-3776AB.svg?style=flat&logo=Python&logoColor=white" alt="Python">
<img src="https://img.shields.io/badge/Pydantic-E92063.svg?style=flat&logo=Pydantic&logoColor=white" alt="Pydantic">

</div>
<br>

---

## Table of Contents

- [Overview](#overview)
- [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
    - [Usage](#usage)
    - [Testing](#testing)

---

## Overview

Polls-app-api is a modern, FastAPI-powered framework for building scalable polling applications with real-time results. It provides a structured, modular API architecture that simplifies creating, managing, and retrieving polls, votes, and results.

**Why polls-app-api?**

This project aims to streamline the development of interactive polling systems. The core features include:

- 🛠️ **API Modularity:** Well-defined endpoints for polls, votes, and results, enabling scalable and maintainable code.
- 🚀 **Fast Performance:** Built on FastAPI, ensuring high-speed request handling and seamless integration.
- 🔑 **Data Validation:** Robust models for votes, options, and polls to maintain data integrity.
- 💾 **Real-Time Data:** Utility functions leveraging Redis for instant vote tracking and result aggregation.
- 📄 **Clear Configuration:** Simplified setup with Pipfile and comprehensive documentation for quick onboarding.

---

## Getting Started

### Prerequisites

This project requires the following dependencies:

- **Programming Language:** Python
- **Package Manager:** Pipenv

### Installation

Build polls-app-api from the source and install dependencies:

1. **Clone the repository:**

    ```sh
    ❯ git clone https://github.com/reyharighy/polls-app-api.git
    ```

2. **Navigate to the project directory:**

    ```sh
    ❯ cd polls-app-api
    ```

3. **Install the dependencies:**

**Using [pipenv](https://pipenv.pypa.io/):**

```sh
❯ pipenv install
```

### Usage

Activate the environment:

**Using [pipenv](https://pipenv.pypa.io/):**

```sh
pipenv shell
```

### Server

Run the FastAPI server with uvicorn:

**Using [pipenv](https://pipenv.pypa.io/):**

```sh
uvicorn app.main:app --reload
```

### Documentation

Interactive API documentation is well-generated with Swagger UI:


```
http://localhost:8000/docs#/
```

---

<div align="left"><a href="#top">⬆ Return</a></div>

---
