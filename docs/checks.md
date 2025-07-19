---
title: Checks
---

## Checks

When your website has been built, how do you know it's correct and working?

StaticPipes can run checks against your website. 

After all if you are writing Python you use linters, type checkers, tests and more to make sure your code is correct and working. Why not do the same for your static website?


### Getting started

The configuration should include (see [Getting Started](../getting_started) for a full example and use):

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

### More information

* [Python reference](../reference/staticpipes.checks.html)

