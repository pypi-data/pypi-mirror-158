# Contributing

Setting up development environment:

```bash
python -m pip install --upgrade pip
python -m pip install flit tox
flit install --symlink
```

Show all available tox tasks:

```bash
tox -av
...
py37     -> testing against python3.7
py38     -> testing against python3.8
py39     -> testing against python3.9
py310    -> testing against python3.10
format   -> format code with black
lint     -> check code style with flake8 and pylint
cover    -> generate code coverage report in html
doc      -> generate sphinx documentation in html
type     -> check type with mypy
```
