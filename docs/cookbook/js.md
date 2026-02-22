---
title: JS Cookbook
---


## JS Cookbook

### Basic

To copy JS files directly, add:

```python
from staticpipes.pipes.copy import PipeCopy

config = Config(
    [
        PipeCopy(extensions=["js"]),
    ],
)
```

### Assets directory

If you like putting your JS in a `assets` directory in your source, you can do:

```python
config = Config(
    [
        PipeCopy(extensions=["js"], source_sub_directory="assets"),
    ],
)
```

Now `assets/js/main.js` will appear in `js/main.js`

### Version

Version your assets:

```python
from staticpipes.pipes.copy_with_versioning import PipeCopyWithVersioning

config = Config(
    [
        PipeCopyWithVersioning(extensions=["js"]),
    ]
)
```

Files like `css/main.js` will still be created, but in the context variables the string `css/main.js?version=ceba641cf86025b52dfc12a1b847b4d8` will be available.

For example, in a Jinja2 template:

```
<script src="{{ versioning_new_filenames['/js/main.js'] }}"></script>
```

You can now get your web server to tell web browsers to cache anything in the `js` folder. Users get the benefit of caching, but if you ever change your JS the link will change and users will see the new version on the next page load.

### Minify


```python
from staticpipes.pipes.javascript_minifier import PipeJavascriptMinifier

config = Config(
    [
        PipeJavascriptMinifier(),
    ],
)
```

### Minify and Version

Use the special Process pipeline to chain together processes, so the same source file goes through multiple steps 
before being published. This minifies then versions JS, putting new filenames in the context for templates to use:

```python
from staticpipes.pipes.process import PipeProcess
from staticpipes.processes.version import ProcessVersion
from staticpipes.processes.javascript_minifier import ProcessJavascriptMinifier

config = Config(
    [
        PipeExcludeUnderscoreDirectories(),
        PipeProcess(extensions=["js"], processors=[ProcessJavascriptMinifier(), ProcessVersion()]),
    ],
)
```

