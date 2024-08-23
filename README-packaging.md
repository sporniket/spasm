# How to build and publish a python package

_See https://packaging.python.org/en/latest/tutorials/packaging-projects/#generating-distribution-archives_

## Pre-checking

```shell
python3 -m pip3 install --upgrade pip
python3 -m pip3 install pdm
python3 -m pdm sync
```

## Run CI locally

```shell
python3 -m pdm run test 
```

## Build and install locally

> This is what is done by the `retest` shell script.


Run test suites with coverage tracking and reporting :

```shell
python3 -m pdm build
python3 -m pip3 install dist/spasm_by_sporniket-<version>-py3-none-any.whl
```

## Publish on pypi

Check list
- [ ] Code complete and passing tests
- [ ] pyproject.toml has the right version
- [ ] Readme up to date (MUST include release notes for the release to publish)
- [ ] Tagged with git using matching version ('v' + version)

Display the token so that a copy/paste is prepared. Then use the login `__token__`, and paste the token as the password.

```shell
python3 -m twine upload --repository pypi dist/*
```
