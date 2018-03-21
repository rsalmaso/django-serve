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


## CHANGES ##


### dev

* initial implementation
* add support for gunicorn config file
* add custom django reloader
* add log-level option
