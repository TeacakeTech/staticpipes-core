---
title: Markdown Cookbook
---


## Markdown Cookbook

### Turn Markdown files into HTML pages with a Jinja2 template

Create `index.md`:

```
---
title: Hello
---

# Hello

And welcome!
```

Create `template.html`:

```
<html>
    <head>
        <title>{{ title }}</title>
    </head>
    <body>
        {{ content | safe}}
    </body>
</html>
```

The HTML of the markdown page will be available in the variable `content` for your Jinja2 templates, and the variables in the YAML block are also available.

Create `site.py`:

```python
from staticpipes.pipes.process import PipeProcess
from staticpipes.processes.jinja2_render_source_file import ProcessJinja2RenderSourceFile
from staticpipes.processes.markdown_yaml_to_html_context import (
    ProcessMarkdownYAMLToHTMLContext,
)
from staticpipes.processes.change_extension import ProcessChangeExtension
from staticpipes.config import Config
import logging
import os

config = Config(
    [
        PipeProcess(
            extensions=["md"],
            processors=[
                ProcessMarkdownYAMLToHTMLContext(),
                ProcessJinja2RenderSourceFile(template="template.html"),
                ProcessChangeExtension("html")
            ],
        ),
    ],
)

if __name__ == "__main__":
    from staticpipes.cli import cli
    cli(
        config,
        os.path.join(os.path.dirname(os.path.realpath(__file__))),
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "_site"),
        log_level=logging.DEBUG,
    )
```

