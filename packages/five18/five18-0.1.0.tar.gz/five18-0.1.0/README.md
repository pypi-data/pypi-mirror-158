# five18

Lightweight library for dealing with your project's pyproject.toml file.

## Installation

```shell
pip install five18
```

## Usage

### Access [tool table](https://peps.python.org/pep-0518/#tool-table) attributes

```python
from five18 import PyProjectToml

pytoml = PyProjectToml()

# get version from poetry tool table
print(pytoml.tool_table.poetry.version)

# get dependencies from poetry tool table
print(pytoml.tool_table.poetry.dependencies)

# get dev dependencies from poetry tool table
print(pytoml.tool_table.poetry.dev_dependencies)
```
