# Copyright (C) 2018, Raffaele Salmaso <raffaele@salmaso.org>
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
except ImportError:
    raise Exception("You need gunicorn to be installed")


class Command(BaseCommand):
    help = _("gunicorn runserver command")

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            "--port",
            action="store",
            dest="port",
            default=self.default_port,
            help="port to bind",
        )
        parser.add_argument(
            "--addr",
            action="store",
            dest="addr",
            default=self.default_addr,
            help="address to bind",
        )
        parser.add_argument(
            "--workers",
            action="store",
            dest="workers",
            default=str(max(2, multiprocessing.cpu_count() - 1)),
            help="workers",
        )
        parser.add_argument(
            "--wsgi",
            action="store",
            dest="wsgi",
            default=self.default_wsgi,
            help="wsgi module to call",
        )
        parser.add_argument(
            "--name",
            action="store",
            dest="name",
            default=self.default_proc_name,
            help="proc name",
        )

    def handle(self, **options):
        sys.argv = [
            "gunicorn",
            "--bind", "{addr}:{port}".format(port=options.get("port"), addr=options.get("addr")),
            "--workers", options.get("workers"),
            "--name", options.get("name"),
            "--log-file", "-",
            "--access-logfile", "-",
            "--error-logfile", "-",
            "--reload",
            "--reload-engine", "auto",
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
