---
title: Getting Started
---

## Getting Started

### Basic configuration

Configure this tool with a simple Python `site.py` in the root of your site. This copies files with these extensions 
into the `_site` directory:

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

### Run

Then run with:

    python site.py build
    python site.py watch
    python site.py serve

### Jinja2

Use Jinja2 templates for html files:

```python
from staticpipes.pipes.jinja2 import PipeJinja2

config = Config(
    pipes=[
        PipeCopy(extensions=["css", "js"]),
        PipeJinja2(extensions=["html"]),
    ],
    context={
        "title": "An example website",
    }
)
```

### Assets directory

If you like putting your CSS and JS in a `assets` directory in your source, you can do:

```python
config = Config(
    pipes=[
        PipeCopy(extensions=["css", "js"], source_sub_directory="assets"),
        PipeJinja2(extensions=["html"]),
    ],
    context={
        "title": "An example website",
    }
)
```

Now `assets/css/main.css` will appear in `css/main.css`

### Version your assets

```python
from staticpipes.pipes.copy_with_versioning import PipeCopyWithVersioning

config = Config(
    pipes=[
        PipeCopyWithVersioning(extensions=["css", "js"]),
        PipeJinja2(extensions=["html"]),
    ]
)
```

Files like `js/main.ceba641cf86025b52dfc12a1b847b4d8.js` will be created, and that string will be available in Jinja2 
variables so you can load them.

### Exclude

Exclude library files like `_layouts/base.html` templates:

```python
from staticpipes.pipes.exclude_underscore_directories import PipeExcludeUnderscoreDirectories

config = Config(
    pipes=[
        PipeExcludeUnderscoreDirectories(),
        PipeCopyWithVersioning(extensions=["css", "js"]),
        PipeJinja2(extensions=["html"]),
    ],
)
```

### Minify

Minify your JS & CSS:

```python
from staticpipes.pipes.javascript_minifier import PipeJavascriptMinifier
from staticpipes.pipes.css_minifier import PipeCSSMinifier

config = Config(
    pipes=[
        PipeExcludeUnderscoreDirectories(),
        PipeJavascriptMinifier(),
        PipeCSSMinifier(),
        PipeJinja2(extensions=["html"]),
    ],
)
```

### Minify and Version

Use the special Process pipeline to chain together processes, so the same source file goes through multiple steps 
before being published. This minifies then versions JS & CSS, putting new filenames in the context for templates to use:

```python
from staticpipes.pipes.process import PipeProcess
from staticpipes.processes.version import ProcessVersion
from staticpipes.processes.javascript_minifier import ProcessJavascriptMinifier
from staticpipes.processes.css_minifier import ProcessCSSMinifier

config = Config(
    pipes=[
        PipeExcludeUnderscoreDirectories(),
        PipeProcess(extensions=["js"], processors=[ProcessJavascriptMinifier(), ProcessVersion()]),
        PipeProcess(extensions=["css"], processors=[ProcessCSSMinifier(), ProcessVersion()]),
        PipeJinja2(extensions=["html"]),
    ],
)
```

### Write your own pipeline

For instance, if you want your robots.txt to block AI crawlers here's all you need:

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

### Check your website

Finally let's add in some checks:

```python
from staticpipes.checks.html_tags import CheckHtmlTags
from staticpipes.checks.internal_links import CheckInternalLinks

config = Config(
    checks=[
        # Checks all img tags have alt attributes
        CheckHtmlTags(),
        # Check all internal links exist
        CheckInternalLinks(),
    ],
)
```

When you build your site, you will now get a report of any problems.
