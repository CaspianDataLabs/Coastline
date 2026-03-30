# Installation

## Requirements

- Python 3.11 or higher
- pip or uv package manager

## Install with pip

```bash
pip install coastline
```

## Install with uv

```bash
uv add coastline
```

## Verify Installation

After installation, verify that Coastline is installed correctly:

```bash
python -c "import coastline; print(coastline.__version__)"
```

## Dependencies

Coastline depends on:

- **pydantic** (>=2.12.5) - For data validation and serialization
- **pyyaml** (>=6.0.3) - For YAML file parsing

These are installed automatically with Coastline.

## Next Steps

Proceed to the [Quick Start](quick-start.md) guide to learn how to use Coastline.
