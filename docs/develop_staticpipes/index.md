---
title: Develop StaticPipes
---

# Develop StaticPipes

If you want to develop the actual tool (instead of just using it to build a website), read on.


## Dev Containers

You can just open a dev container to get an environment with all the features you need.

To see an example site, run:

```
python docs.py s
```

And go to [http://localhost:8000/](http://localhost:8000/)

## Docker

You can also open a Docker container to get an environment with all the features you need.

To setup:

```
docker build -t staticpatchdevcontainer  -f Dockerfile.devcontainer .
```

To run:

```
docker run --rm -it --name staticpatchdevcontainer -v .:/workspace -p 8000:8000 staticpatchdevcontainer bash
```

To see an example site, run:

```
python docs.py s -a 0.0.0.0
```

And go to [http://localhost:8000/](http://localhost:8000/)

## Test

Run:

```
pytest tests/
```

## Lint

Run:

```
black staticpipes tests docs.py
isort staticpipes tests docs.py
flake8 staticpipes tests docs.py
mypy --install-types --non-interactive -p staticpipes
```

