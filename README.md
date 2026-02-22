# StaticPipes - the unopinionated static website generator in Python that checks the output for you

Most static website generators have technologies, conventions and source code layout requirements that you have to 
follow. 

Instead this is a framework and a collection of pipes and processes to build a website from your source files. 
Use only the pipes and processes you want and configure them as you need. 

If you are a Python programmer and need something different, then write a Python class that extends our base class and 
write what you need.

Finally, when your site is built we will check the output for you - after all you check your code with all kinds of linters, 
so why not check your static website too?

## Install

* `pip install staticpipes[allbuild]` - if you just want to build a website
* `pip install staticpipes[allbuild,dev]` - if you want to develop a website

If you are developing the actual tool, check it out from git, create a virtual environment and run 
`python3 -m pip install --upgrade pip && pip install -e .[allbuild,dev,staticpipesdev]`

## Getting started - build your site

Configure this tool with a simple Python `site.py` in the root of your site. This copies files with these extensions 
into the `_site` directory:

```python
from staticpipes.config import Config
from staticpipes.pipes.copy import PipeCopy

import os

config = Config(
    [
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

Then run with:

    python site.py build
    python site.py watch
    python site.py serve

Use Jinja2 templates for html files:

```python
from staticpipes.pipes.jinja2 import PipeJinja2

config = Config(
    [
        PipeCopy(extensions=["css", "js"]),
        PipeJinja2(extensions=["html"]),
    ],
    context={
        "title": "An example website",
    }
)
```

If you like putting your CSS and JS in a `assets` directory in your source, you can do:

```python
config = Config(
    [
        PipeCopy(extensions=["css", "js"], source_sub_directory="assets"),
        PipeJinja2(extensions=["html"]),
    ],
    context={
        "title": "An example website",
    }
)
```

(Now `assets/css/main.css` will appear in `css/main.css`)

Version your assets:

```python
from staticpipes.pipes.copy_with_versioning import PipeCopyWithVersioning

config = Config(
    [
        PipeCopyWithVersioning(extensions=["css", "js"]),
        PipeJinja2(extensions=["html"]),
    ]
)
```

(files like `js/main.ceba641cf86025b52dfc12a1b847b4d8.js` will be created, and that string will be available in Jinja2 
variables so you can load them.)

Exclude library files like `_layouts/base.html` templates:

```python
from staticpipes.pipes.exclude_underscore_directories import PipeExcludeUnderscoreDirectories

config = Config(
    [
        PipeExcludeUnderscoreDirectories(),
        PipeCopyWithVersioning(extensions=["css", "js"]),
        PipeJinja2(extensions=["html"]),
    ],
)
```

Minify your JS & CSS:

```python
from staticpipes.pipes.javascript_minifier import PipeJavascriptMinifier
from staticpipes.pipes.css_minifier import PipeCSSMinifier

config = Config(
    [
        PipeExcludeUnderscoreDirectories(),
        PipeJavascriptMinifier(),
        PipeCSSMinifier(),
        PipeJinja2(extensions=["html"]),
    ],
)
```

Use the special Process pipeline to chain together processes, so the same source file goes through multiple steps 
before being published. This minifies then versions JS & CSS, putting new filenames in the context for templates to use:

```python
from staticpipes.pipes.process import PipeProcess
from staticpipes.processes.version import ProcessVersion
from staticpipes.processes.javascript_minifier import ProcessJavascriptMinifier
from staticpipes.processes.css_minifier import ProcessCSSMinifier

config = Config(
    [
        PipeExcludeUnderscoreDirectories(),
        PipeProcess(extensions=["js"], processors=[ProcessJavascriptMinifier(), ProcessVersion()]),
        PipeProcess(extensions=["css"], processors=[ProcessCSSMinifier(), ProcessVersion()]),
        PipeJinja2(extensions=["html"]),
    ],
)
```

Or write your own pipeline! For instance, if you want your robots.txt to block AI crawlers here's all you need:

```python
from staticpipes.pipe_base import BasePipe
import requests

class PipeNoAIRobots(BasePipe):
    def start_build(self, current_info) -> None:
        r = requests.get("https://raw.githubusercontent.com/ai-robots-txt/ai.robots.txt/refs/heads/main/robots.txt")
        r.raise_for_status()
        self.build_directory.write("/", "robots.txt", r.text)

config = Config(
    [
        PipeNoAIRobots(),
    ],
)
```
## Getting started - check your website

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

## More information and feedback

* Documentation in the `docs` directory
* https://github.com/StaticPipes/StaticPipes



