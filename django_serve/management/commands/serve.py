# Copyright (C) 2018-2020, Raffaele Salmaso <raffaele@salmaso.org>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import multiprocessing
import os
import sys

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.functional import cached_property
from django.utils.translation import gettext as _

try:
    from gunicorn.app.wsgiapp import WSGIApplication
    from gunicorn import reloader
except ImportError:
    raise Exception("You need gunicorn to be installed")

try:
    import gunicorn_color  # noqa: F401

    logger_class = "gunicorn_color.Logger"
except ImportError:
    logger_class = None


class DjangoReloader(reloader.InotifyReloader):
    """Patch InotifyReloader to process only py files"""

    def run(self):
        self._dirs = self.get_dirs()

        for dirname in self._dirs:
            self._watcher.add_watch(dirname, mask=self.event_mask)

        for event in self._watcher.event_gen():
            if event is None:
                continue

            filename = event[3]
            if filename.endswith((".py", ".env", ".mo")):
                self._callback(filename)


reloader.preferred_reloader = DjangoReloader
reloader.reloader_engines["django"] = DjangoReloader


class Command(BaseCommand):
    help = _("gunicorn runserver command")

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            "--config", action="store", dest="config", help="config file",
        )
        parser.add_argument(
            "--port", action="store", dest="port", default=self.default_port, help="port to bind",
        )
        parser.add_argument(
            "--addr", action="store", dest="addr", default=self.default_addr, help="address to bind",
        )
        parser.add_argument(
            "--workers",
            action="store",
            dest="workers",
            default=str(max(2, multiprocessing.cpu_count() - 1)),
            help="workers",
        )
        parser.add_argument(
            "--wsgi", action="store", dest="wsgi", default=self.default_wsgi, help="wsgi module to call",
        )
        parser.add_argument(
            "--name", action="store", dest="name", default=self.default_proc_name, help="proc name",
        )
        parser.add_argument(
            "--logformat", action="store", dest="logformat", default=self.default_logformat, help="log format",
        )
        parser.add_argument(
            "--logger-class",
            action="store",
            dest="logger_class",
            default=logger_class,
            help="the logger you want to use to log events",
        )
        parser.add_argument(
            "--log-level",
            action="store",
            dest="loglevel",
            default="info",
            help="granularity of error log outputs (debug, info, warning, error, critical)",
        )

    def get_config(self, options):
        config = options.get("config")
        if config:
            return ["--config", config]
        return []

    def get_logger_class(self, options):
        logger_class = options.get("logger_class")
        if logger_class:
            return ["--logger-class", logger_class]
        return []

    def handle(self, **options):
        sys.argv = [
            "gunicorn",
            *self.get_config(options),
            "--bind",
            "{addr}:{port}".format(port=options.get("port"), addr=options.get("addr")),
            "--workers",
            options.get("workers"),
            "--name",
            options.get("name"),
            "--log-file",
            "-",
            "--access-logformat",
            options.get("logformat"),
            "--access-logfile",
            "-",
            "--error-logfile",
            "-",
            "--log-level",
            options.get("loglevel"),
            *self.get_logger_class(options),
            "--reload",
            "--reload-engine",
            "django",
            options.get("wsgi"),
        ]
        WSGIApplication("").run()

    @cached_property
    def default_port(self):
        return self.get_default_port()

    def get_default_port(self):
        return os.environ.get("DJANGO_DEFAULT_PORT", "8000")

    @cached_property
    def default_addr(self):
        return self.get_default_addr()

    def get_default_addr(self):
        return os.environ.get("DJANGO_DEFAULT_ADDR", "127.0.0.1")

    @cached_property
    def default_proc_name(self):
        return self.get_default_proc_name()

    def get_default_proc_name(self):
        return os.environ.get("DJANGO_DEFAULT_PROC_NAME", "django")

    @cached_property
    def default_wsgi(self):
        return self.get_default_wsgi()

    def get_default_wsgi(self):
        app = settings.WSGI_APPLICATION.split(".")
        app = "{}:{}".format(".".join(app[:-1]), app[-1])
        return os.environ.get("DJANGO_DEFAULT_WSGI", app)

    @property
    def default_logformat(self):
        return self.get_default_logformat()

    def get_default_logformat(self):
        return os.environ.get("LOG_FORMAT", '"%(m)s %(U)s%(q)s %(H)s" %(s)s %(B)s')
