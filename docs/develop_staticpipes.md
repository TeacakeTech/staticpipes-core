---
title: Develop StaticPipes
---

## Develop StaticPipes

If you want to develop the actual tool (instead of just using it to build a website), read on.


### Dev Containers

You can just open a dev container to get an environment with all the features you need.

To see the docs site, run:

```
python docs.py s
```

And go to port 8000 on the correct host.

### Docker

You can also open a Docker container to get an environment with all the features you need.

To setup:

```
docker build -t staticpipesdevcontainer  -f Dockerfile.devcontainer .
```

To run:

```
docker run --rm -it --name staticpipesdevcontainer -v .:/workspace -p 8000:8000 staticpipesdevcontainer bash
```

To see the docs site, run:

```
python docs.py s -a 0.0.0.0
```

And go to [http://localhost:8000/](http://localhost:8000/)

### Test

If inside the dev container or Docker, just run:

```
test
```

### Lint

If inside the dev container or Docker, just run:

```
lint
```

