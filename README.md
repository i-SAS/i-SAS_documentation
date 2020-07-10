# i-SAS_documentation
documentation for integrate Structural Analysis System

## 1. Clone
```
$ git clone https://github.com/i-SAS/i-SAS_documentation
$ cd i-SAS_documentation
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

#### Update Document
```
# python documentation/bin/update_documentation.py
```
