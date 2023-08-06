# different utils and tools for projects

collecting python modules into library.

needs VTK
```bash
brew install vtk
```

## install from pypi

```bash

pip install laapyCore

```

## install from source

to work on project install source locally, activate venv and run (if mac run zsh version):

```bash

pip install -e .[dev]

```

```zsh

pip install -e '.[dev]'

```

## use

```python

from working_tools import tet

```

## test setup state

```zsh
python setup.py sdist
```


## create manifest

```zsh

check-manifest --create
git add MANIFEST.in

```

## build to upload

```bash
python setup.py bdist_wheel sdist

twine upload dist/*
```
