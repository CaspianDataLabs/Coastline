# Stage 1: Base image with dependencies installation
FROM python:3.14-slim AS builder

WORKDIR /app

ENV POETRY_VIRTUALENVS_IN_PROJECT=True

# Install Poetry
RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | python -

# Copy project files
COPY . .

# Configure Poetry
ENV PATH="/root/.local/bin:$PATH"
RUN poetry config virtualenvs.create true
RUN poetry config virtualenvs.in-project true
RUN poetry config virtualenvs.path .venv

# Install dependencies
RUN poetry install --without dev --no-interaction

# Stage 2: Runtime image
FROM python:3.14-slim AS runtime

WORKDIR /app

# Copy dependencies from builder stage
COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/pyakmc /app/pyakmc
ENV PATH="/app/.venv/bin:$PATH"

# Set startup command
ENTRYPOINT ["pyakmc"]
