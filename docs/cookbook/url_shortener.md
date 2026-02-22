---
title: URL Shortener
---

## URL Shortener

Here's how to create a URL Shortener system.

### Data about the URLs

Create some source data in the way that can be loaded into a collection.

A CSV is simplest, but see the documentation on collections for more options.

Create a CSV called `data.csv` with the contents:

```
Id,URL
python,https://www.python.org/
```

### Create site

Create a template called `template.html` with the contents:

```
<html>
    <head>
        <meta http-equiv="refresh" content="0; url={{ link["URL"] }}">.
    </head>
    <body>
        <p><a href="{{ link["URL"] }}">Please go to {{ link["URL"] }}</a></p>
    </body>
</html>

```

Create a Python file called `site.py` with the contents:

```
import logging
import os

from staticpipes.pipes.load_collection_csv import PipeLoadCollectionCSV
from staticpipes.pipes.collection_records_process import PipeCollectionRecordsProcess
from staticpipes.processes.jinja2_render_source_file import ProcessJinja2RenderSourceFile
from staticpipes.config import Config

config = Config(
    [
        PipeLoadCollectionCSV(filename="data.csv", collection_name="links"),
        PipeCollectionRecordsProcess(
            collection_name="links",
            context_key_record_data="link",
            output_mode="dir",
            output_dir="/",
            processors=[
                ProcessJinja2RenderSourceFile(
                    template="template.html",
                ),
            ],
        ),
    ]
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

Run: `python site.py s`

If you open [http://localhost:8000/python](http://localhost:8000/python) you should be redirected to the Python site.

### Add a interstitial page with a custom message for each URL

Edit the CSV called `data.csv` to add a message:

```
Id,URL,Message
python,https://www.python.org/,Python is a great programming language
```


Edit the template called `template.html` to:

```
<html>
    <head>
    </head>
    <body>
        <p><a href="{{ link["URL"] }}">Please go to {{ link["URL"] }}</a></p>
        <p>{{ link["Message"] }}</p>
    </body>
</html>
```

Run: `python site.py s`

If you open [http://localhost:8000/python](http://localhost:8000/python) you should see a page with a link and your custom message.

### Put all your URLs in a sub directory

If you want to use this as part of another site (say alongside a blog), you probably want all your URLs in a subdirectory.

Edit the Python file called `site.py` and for `PipeCollectionRecordsProcess` change the value of `output_dir` to `urls`.

Run: `python site.py s`

Now open [http://localhost:8000/urls/python](http://localhost:8000/urls/python).

