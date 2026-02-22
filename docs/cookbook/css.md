---
title: CSS Cookbook
---


## CSS Cookbook

### Basic

To copy CSS files directly, add:

```python
from staticpipes.pipes.copy import PipeCopy

config = Config(
    [
        PipeCopy(extensions=["css"]),
    ],
)
```

### Assets directory

If you like putting your CSS in a `assets` directory in your source, you can do:

```python
config = Config(
    [
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
    [
        PipeCopyWithVersioning(extensions=["css"]),
    ]
)
```

Files like `css/main.css` will still be created, but in the context variables the string `css/main.css?version=ceba641cf86025b52dfc12a1b847b4d8` will be available.

For example, in a Jinja2 template:

```
<link href="{{ versioning_new_filenames['/css/main.css'] }}" rel="stylesheet"/>
```

You can now get your web server to tell web browsers to cache anything in the `css` folder. Users get the benefit of caching, but if you ever change your CSS the link will change and users will see the new version on the next page load.

### Minify


```python
from staticpipes.pipes.css_minifier import PipeCSSMinifier

config = Config(
    [
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
    [
        PipeExcludeUnderscoreDirectories(),
        PipeProcess(extensions=["css"], processors=[ProcessCSSMinifier(), ProcessVersion()]),
    ],
)
```

