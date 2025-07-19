---
title: Collections
---

## Collections

Collections are a way you can load a set of data from sources (either internal or external) and use that when building your website.

Load data via different pipes (depending on it's source).

Then use:

* via variables in Jinja2 or other templates
* via a pipe that will run processes for each item in the collection.


### Getting started

Create a CSV file `pets.csv`:

```
pet,floffy
cat,very
dog,yes
```

Create a template file `_templates/pet.html`:

```
<html>
    <body>
        {{ record_id }} is floffy? {{ record_data.floffy }}
    </body>
</html>
```

The configuration should include (see [Getting Started](../getting_started) for a full example and use):

```python
from staticpipes.pipes.load_collection_csv import PipeLoadCollectionCSV
from staticpipes.pipes.collection_records_process import PipeCollectionRecordsProcess
from staticpipes.processes.jinja2 import ProcessJinja2

config = Config(
    pipes=[
        PipeLoadCollectionCSV(filename="pets.csv",collection_name="pets"),
        PipeCollectionRecordsProcess(
            collection_name="pets",
            processors=[
                ProcessJinja2(
                    template="_templates/pet.html",
                )
            ],
            output_dir="pets",
        ),
    ],
)
```

This will create output files `pets/cat.html` and `pets/dog.html`.

This can output any file type, not just html - so it could output a JSON file of data for each record to make an API, for instance.

### Use with DataTig

If you are crowd sourcing data in a git repository, we recommend using the collections feature in combination with [DataTig](https://www.datatig.com/). This open source tool provides many features such as:

* web forms to help people contribute new data or edit existing data
* checking data quality
* transforming the data to many formats 
* providing a static website with browsing, downloads and API

### More information

* Python reference
    * [Loading](../reference/staticpipes.pipes.html) see pipes that start load_collection
    * [Using](../reference/staticpipes.pipes.collection_records_process.html) 

