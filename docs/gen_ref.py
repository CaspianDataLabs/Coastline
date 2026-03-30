#!/usr/bin/env python3
"""Script to generate API reference documentation from source code."""

from pathlib import Path


def generate_api_ref():
    docs_dir = Path(__file__).parent
    api_ref_path = docs_dir / "api.md"

    src_dir = Path(__file__).parent.parent / "src" / "coastline"

    content = [
        "# API Reference",
        "",
        "This page is auto-generated from the source code.",
        "",
        "## Functions",
        "",
        "### `config`",
        "",
        "Decorator to register a class with the config registry.",
        "",
        "```python",
        "def config(cls: type | None = None, *, name: str | None = None)",
        "```",
        "",
        "**Parameters:**",
        "",
        "- `cls` (type, optional): The class to decorate.",
        "- `name` (str, optional): Custom name for the registry key.",
        "",
        "---",
        "",
        "## Classes",
        "",
    ]

    # Read source files
    for filename in ["registry.py", "loader.py"]:
        filepath = src_dir / filename
        if filepath.exists():
            class_name = (
                filename.replace(".py", "").replace("_", "").title().replace(".py", "")
            )
            content.append(f"### {class_name}")
            content.append("")
            content.append(f"Source: `{filename}`")
            content.append("")

    api_ref_path.write_text("\n".join(content))
    print(f"Generated {api_ref_path}")


if __name__ == "__main__":
    generate_api_ref()
