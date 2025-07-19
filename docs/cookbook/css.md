---
title: CSS Cookbook
---


## CSS Cookbook

### Basic

To copy CSS files directly, add:

```python
from staticpipes.pipes.copy import PipeCopy

config = Config(
    pipes=[
        PipeCopy(extensions=["css"]),
    ],
)
```

### Assets directory

If you like putting your CSS in a `assets` directory in your source, you can do:

```python
config = Config(
    pipes=[
        PipeCopy(extensions=["css"], source_sub_directory="assets"),
    ],
)
```

Now `assets/css/main.css` will appear in `css/main.css`

### Version 

Version your assets:

```python
from staticpipes.pipes.copy_with_versioning import PipeCopyWithVersioning

config = Config(
    pipes=[
        PipeCopyWithVersioning(extensions=["css"]),
    ]
)
```

Files like `css/main.ceba641cf86025b52dfc12a1b847b4d8.js` will be created, and that string will be available in context 
variables so you can load them. 

For example, in a Jinja2 template:

```
<link href="{{ versioning_new_filenames['/css/main.css'] }}" rel="stylesheet"/>
```

You can now get your webserver to tell web browsers to cache anything in the `css` folder. Users get the benifit of caching, but if you ever change your CSS the filename will change and users will see a new version on the next page load.

### Minify


```python
from staticpipes.pipes.css_minifier import PipeCSSMinifier

config = Config(
    pipes=[
        PipeCSSMinifier(),
    ],
)
```

### Minify and Version

Use the special Process pipeline to chain together processes, so the same source file goes through multiple steps 
before being published. This minifies then versions CSS, putting new filenames in the context for templates to use:

```python
from staticpipes.pipes.process import PipeProcess
from staticpipes.processes.version import ProcessVersion
from staticpipes.processes.css_minifier import ProcessCSSMinifier

config = Config(
    pipes=[
        PipeExcludeUnderscoreDirectories(),
        PipeProcess(extensions=["css"], processors=[ProcessCSSMinifier(), ProcessVersion()]),
    ],
)
```

