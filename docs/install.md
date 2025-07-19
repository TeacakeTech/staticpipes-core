---
title: Install
---

## Install

### From PyPi

* `pip install staticpipes[allbuild]` - if you just want to build a website
* `pip install staticpipes[allbuild,dev]` - if you want to develop a website

If you are developing the actual tool, check it out from git, create a virtual environment and run 
`python3 -m pip install --upgrade pip && pip install -e .[allbuild,dev,staticpipesdev]`
