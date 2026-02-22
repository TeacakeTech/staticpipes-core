---
title: Source Layout
---

## Source Layout

### Everything in same directory

You can have the `site.py` and all the source files in the same directory.

In this case, in your `site.py` the main block would have:

```python
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

If this directory is also a git repository, you can stop the `.git` repository being processed with:

```python
from staticpipes.pipes.exclude_dot_directories import PipeExcludeDotDirectories

config = Config(
    [
        PipeExcludeDotDirectories(),
        # rest of the pipes
    ],
)
```

### All source files in a special directory

However, you may then want to add other files into a git repository that don't belong 
in your final site (like `.gitignore`).

You can do various things to exclude them or make sure they are not copied to the final 
site, but it may be easier to have all your source files in a directory called `src` next to `site.py`.

In this case, in your `site.py` the main block would have:

```python
if __name__ == "__main__":
    from staticpipes.cli import cli
    cli(
        config, 
        # The source directory - "src" in the same place as this file is in
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "src"), 
        # The build directory - _site directory below this file (It will create it for you!)
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "_site")
    )
```

### Different directories for different things inside your source

If you like putting your CSS and JS in a `assets` directory in your source, you can do:

```python
config = Config(
    [
        PipeCopy(extensions=["css", "js"], source_sub_directory="assets"),
    ],
)
```

Now `assets/css/main.css` in your source directory will appear in `css/main.css` in your site.

