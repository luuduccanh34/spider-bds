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

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Contact
For questions or contributions, please contact the project maintainer at [your-email@example.com].
