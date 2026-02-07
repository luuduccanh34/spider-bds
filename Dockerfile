# Use 3.12 to match what your Pipfile requires
FROM python:3.12-slim

WORKDIR /app

# Best Practice: Copy BOTH Pipfile and Pipfile.lock
# This avoids the need to run 'pipenv lock' during the build
COPY Pipfile Pipfile.lock ./

RUN pip install pipenv

# Install dependencies directly into the container's system python
# This avoids the complexity of nested virtual environments in Docker
RUN pipenv install --system --deploy

COPY . .

# No need to modify PATH if using --system
CMD ["python", "main.py"]