# Multiservice

Multiservice (`ms`) is a tool to run the same commands on multiple services.

## Install

```console
$ pip install multiservice
```


## Usage

```console
$ multiservice [OPTIONS] COMMAND [SERVICES]...
```

**Options**:

* `-c, --config TEXT`: [default: ~/.multiservice.yml]
* `COMMAND`: [required]: command name from the config
* `[SERVICES]...`: a list of services aliases


**Examples**:

Run a command named `status` on all services:
```console
$ ms status
```

Run a command named `status` on some services:
```console
$ ms status as rs
```

Execute custom script
```console
$ ms execute --execute 'git status && git diff' as rs
```

Edit the config file
```console
$ ms edit
```

## Configuration
Multiservice uses a config file to define commands and services.
Default path is `~/.multiservice.yml`, but you can specify a path using `--config` or `-c` options.

Config example:
```yaml
root: ~/projects/
template: source ./venv/bin/activate && {COMMAND}

editor: vim

# alias: directory
services:
  as: attributes-service
  rs: reports-service

commands:
  status: git status
  reset: git reset origin/develop --hard
  pull: >
    git checkout develop -q &&
    git pull
```
