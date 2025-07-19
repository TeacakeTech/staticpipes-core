---
title: Markdown Cookbook
---


## Markdown Cookbook

### Turn Markdown files into HTML pages with a Jinja2 template

```python
from staticpipes.pipes.process import PipeProcess
from staticpipes.processes.jinja2 import ProcessJinja2
from staticpipes.processes.markdown_yaml_to_html_context import (
    ProcessMarkdownYAMLToHTMLContext,
)

config = Config(
    pipes=[
        PipeProcess(
            extensions=["md"],
            processors=[
                ProcessMarkdownYAMLToHTMLContext(),
                ProcessJinja2(template="_templates/content.html"),
            ],
        ),
    ],
)
```

The HTML will be available in the variable content for your Jinja2 templates:

```
{{ content | safe}}
```

<!-- describe how YAML blocks are turned into variables, when that works properly -->

