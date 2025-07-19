---
title: Run
---

## Run

### Configure

Once your website is setup, you will have a `site.py` or other python file with all the details.

Here is a basic example:

```python
from staticpipes.config import Config
from staticpipes.pipes.copy import PipeCopy

import os

config = Config(
    pipes=[
        PipeCopy(extensions=["html", "css", "js"]),
    ],
)

if __name__ == "__main__":
    from staticpipes.cli import cli
    cli(
        config, 
        # The source directory - same directory as this file is in
        os.path.dirname(os.path.realpath(__file__)), 
        # The build directory - _site directory below this file (It will create it for you!)
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "_site")
    )
```

### Build

    python site.py build

### Watch

    python site.py watch

### Serve

    python site.py serve

