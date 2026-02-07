# Spider-BDS

## Project Description
Spider-BDS is a data engineering utility designed to streamline the process of uploading data to Google Cloud Storage (GCS). The project demonstrates how to create a sample DataFrame, configure GCS settings, and upload the data using the `GCSClient` class. It is containerized using Docker for ease of deployment.

## Features
- Create and manipulate data using `pandas`.
- Upload data to GCS with customizable configurations.
- Environment variable support for dynamic settings.
- Dockerized for consistent and portable execution.

## Installation

### Prerequisites
- Python 3.12
- Docker (optional, for containerized execution)

### Steps
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd spider-bds
   ```
2. Install dependencies using `pipenv`:
   ```bash
   pip install pipenv
   pipenv install
   ```
3. Set up environment variables:
   - Create a `.env` file in the root directory.
   - Define the following variables:
     ```env
     GCS_BUCKET_NAME=your-bucket-name
     GCS_PREFIX=your-prefix
     GCS_FILE_NAME=your-file-name
     GCS_FILE_FORMAT=csv
     ```

## Usage

### Running Locally
1. Activate the `pipenv` environment:
   ```bash
   pipenv shell
   ```
2. Run the main script:
   ```bash
   python main.py
   ```

### Running with Docker
1. Build the Docker image:
   ```bash
   docker build -t spider-bds .
   ```
2. Run the container:
   ```bash
   docker run --env-file .env spider-bds
   ```

## Development

### Testing
Run tests using `pytest`:
```bash
pipenv run pytest
```

### Linting
Format and lint code using `black` and `flake8`:
```bash
pipenv run lint
```

## Continuous Integration with GitHub Actions

This project uses GitHub Actions to automate the CI workflow. The CI pipeline includes testing, linting, and building the Docker image to ensure code quality and consistency.

### Setting Up GitHub Actions
1. Navigate to the `.github/workflows` directory in the repository.
2. Create a new workflow file (e.g., `ci.yml`) to define the CI pipeline.
3. Use the following video as a reference for setting up the workflow: [GitHub Actions Tutorial](https://www.youtube.com/watch?v=RgZyX-e6W9E).

### Example Workflow
Below is an example of a GitHub Actions workflow for this project:
```yaml
name: CI

on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.12'

    - name: Install dependencies
      run: |
        pip install pipenv
        pipenv install --dev

    - name: Run tests
      run: pipenv run pytest

  lint:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.12'

    - name: Install dependencies
      run: |
        pip install pipenv
        pipenv install --dev

    - name: Run linting
      run: pipenv run lint

  docker:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v3

    - name: Build Docker image
      run: docker build -t spider-bds .
```

### Benefits
- Automates testing and linting to catch issues early.
- Ensures consistent Docker builds.
- Provides feedback directly in pull requests.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Contact
For questions or contributions, please contact the project maintainer at [your-email@example.com].
