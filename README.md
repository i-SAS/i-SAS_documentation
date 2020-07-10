# i-SAS_template
implementation of {package_name} for integrate Structural Analysis System

## 1. Clone
```
$ git clone https://github.com/i-SAS/i-SAS_template
$ cd i-SAS_template
```

## 2. Docker build & run
```
$ docker-compose build
$ docker-compose run --rm package
```

## 3. Command
#### Add package
Modify `pyproject.toml` and command
```
# poetry lock
```

#### Check coding conventions
```
# flake8
```

#### Run test
```
# python -m unittest
```

#### Update Document
```
# sphinx-apidoc -f -o $WORKDIR/docs/source .
# sphinx-build -b singlehtml $WORKDIR/docs/source $WORKDIR/docs/_build
```
