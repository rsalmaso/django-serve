# django-serve

A gunicorn based django runserver command.


## Install ##

`python3 -m pip install django-serve`

and add to `INSTALLED_APPS`

```
#!python
INSTALLED_APPS = [
    ...
    "django_serve.apps.ServeConfig",
    ...
]
```

## Usage ##

```!shell
./manage.py serve
```

### options

* `--addr` The socket address to bind [default=127.0.0.1]
* `--port` The socket port to bind [default=8000]
* `--workers` The number of worker processes for handling requests [default max(2, cpu - 1)]
* `--name` A base to use with setproctitle for process naming [default=django]
* `--wsgi` Dotted path to wsgi application [default=settings.WSGI_APPLICATION]
* `--config' The Gunicorn config file [default=None]
* `--log-level` The granularity of Error log outputs (debug, info, warning, error, critical) [default=info]
* `--logformat` The access log format (default='"%(m)s %(U)s%(q)s %(H)s" %(s)s %(B)s' same as default django runserver)
* `--logger-class` The logger you want to use to log events [default=gunicorn_color.Logger if installed else gunicorn default one]


## CHANGES ##

### dev

* use black
* drop Python 3.5 support
* add Django 3.2 support
* add Python 3.9 and 3.10 support
* add django-serve command
* add support for python -m django_serve
* install inotify only on linux platform

### 0.1.1

* add gunicorn-color as required

### 0.1.0

* initial implementation
* add support for gunicorn config file
* add custom django reloader
* add log-level option
* add logformat configuration
* add logger-class option
