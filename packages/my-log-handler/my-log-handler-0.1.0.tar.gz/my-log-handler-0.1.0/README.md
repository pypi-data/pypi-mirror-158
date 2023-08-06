# logHandler

## Project description

logHander is a simple package to create log. I copy paste same file in all of my project.
I decided to create thid as a package and simply import it.
Currently limited to basic functionality but plans to upgrade it in future.

![Tests](https://github.com/bonnybabukachappilly/utils/actions/workflows/test.yml/badge.svg)

## Features

* Simple add basic log functionality.
* logs to console.

## Installation

```cmd
pip install logHander
```

## Ussage

```python
from logHandler import Logger
Logger('path to log folder', 'log name', [optional] log_level)

# somewhere in the package
import logging
log = logging.getLogger('log name')
log.info("Hello There")

```

## Development

To install logHandler along with tools for developnment and testing run following command.

```cmd
pip install -e .[dev]
```
