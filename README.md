# Duplicates

![Build result](https://travis-ci.org/LucaLanziani/Duplicates.svg?branch=master)

The aim of the project is to provide an easy tool to find duplicated files in a directory. And compare two directories content.

# Prerequirements

The easyest way to start developing is to use a **virtualenv**.

To install the virtualenv check the instruction on the project page: [Virtualenv](https://virtualenv.readthedocs.org/en/latest/installation.html)

# Development enviroment

### Create the virtualenv:

```bash
make ENV
```

you should now find a `env` directory in the project.

### Enter the virtualenv

```bash
source env/bin/activate
```

### Install packages

```bash
make UPDATE_ENV
```

### Test the project

```bash
./bin/duplicates --index --no-store --progress --log-level=DEBUG test/files
```

## Enjoy the development

# Setup Git hooks

It would be a good idea to setup the git hooks to test the project before the commit and the push, the following are the suggested hooks for the project.

### .git/hooks/pre-commit

```bash
#!/bin/bash
make FLAKE8
```

### .git/hooks/pre-push

```bash
#!/bin/sh
remot="$1"
url="$2"
make TESTS
```
