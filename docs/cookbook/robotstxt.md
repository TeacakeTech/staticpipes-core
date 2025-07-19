---
title: Robots.txt cookbook
---


## Robots.txt Cookbook

### Basic

To copy any text file directly, add:

```python
from staticpipes.pipes.copy import PipeCopy

config = Config(
    pipes=[
        PipeCopy(extensions=["txt"]),
    ],
)
```

### Use a robots.txt that attempts to block AI crawlers

You can write a custom pipeline to do this:


```python
from staticpipes.pipe_base import BasePipe
import requests

class PipeNoAIRobots(BasePipe):
    def start_build(self, current_info) -> None:
        r = requests.get("https://raw.githubusercontent.com/ai-robots-txt/ai.robots.txt/refs/heads/main/robots.txt")
        r.raise_for_status()
        self.build_directory.write("/", "robots.txt", r.text)

config = Config(
    pipes=[
        PipeNoAIRobots(),
    ],
)
```

Note this will call raw.githubusercontent.com on every build, and you should add some kind of caching to avoid getting ratelimited while frequently building.

