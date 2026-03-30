# Contributing to Coastline

Thank you for your interest in contributing to Coastline!

## Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/kwierman/coastline.git
   cd coastline
   ```

2. Install dependencies using uv:
   ```bash
   uv sync
   ```

3. Install development dependencies:
   ```bash
   uv sync --group dev
   ```

## Running Tests

Run the test suite:

```bash
uv run pytest
```

Run tests with coverage:

```bash
uv run pytest --cov=src/coastline --cov-report=html
```

## Code Style

This project uses [Ruff](https://github.com/astral-sh/ruff) for linting:

```bash
uv run ruff check .
```

Format code:

```bash
uv run ruff format .
```

## Project Structure

```
coastline/
├── src/coastline/       # Main package
│   ├── __init__.py       # Public API
│   ├── base.py           # @config decorator
│   ├── loader.py         # ConfigLoader
│   └── registry.py       # Registry
├── tests/                # Test suite
├── docs/                 # Documentation
└── examples/             # Example usage
```

## Submitting Changes

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Reporting Issues

Please report issues on the [GitHub issue tracker](https://github.com/kwierman/coastline/issues).

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
