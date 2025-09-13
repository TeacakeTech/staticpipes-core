---
title: Jinja2 Cookbook
---

## Jinja2 Cookbook

Use Jinja2 templates for HTML files:

```python
from staticpipes.pipes.jinja2 import PipeJinja2

config = Config(
    pipes=[
        PipeJinja2(extensions=["html"]),
    ],
    context={
        "title": "An example website",
    }
)
```

The context is available as variables in your templates.

### Exclude library files

It's common to use includes or extends with Jinja2, but you don't want your library template files in the final website.

Put them all in a directory that starts with a `_` like `_templates` then exclude those directories:

```python
from staticpipes.pipes.exclude_underscore_directories import PipeExcludeUnderscoreDirectories

config = Config(
    pipes=[
        PipeExcludeUnderscoreDirectories(),
        PipeJinja2(extensions=["html"]),
    ],
)
```

### Customise Jinja2: filters, autoescape

You can create a custom environment:

```python
from staticpipes.jinja2_environment import Jinja2Environment

jinja2_environment = Jinja2Environment()

# use in config ...
# PipeJinja2(jinja2_environment=jinja2_environment)
# ProcessJinja2RenderSourceFile(jinja2_environment=jinja2_environment)
# ProcessJinja2RenderContents(jinja2_environment=jinja2_environment)
```

You can then change autoescape:

```python
jinja2_environment = Jinja2Environment(autoescape=False)
```

Or add filters:

```python
from markdown_it import MarkdownIt

def render_markdown(content):
    md = MarkdownIt()
    return md.render(content) if content else ""

jinja2_environment = Jinja2Environment(filters={"render_markdown": render_markdown})
```

