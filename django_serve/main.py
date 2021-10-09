# Copyright (C) 2018-2021, Raffaele Salmaso <raffaele@salmaso.org>
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

import os
import sys

try:
    from gunicorn.app.wsgiapp import WSGIApplication
    from gunicorn import reloader
except ImportError:
    raise Exception("You need gunicorn to be installed")


class InotifyReloader(reloader.InotifyReloader):
    """Patch InotifyReloader to process only py, .env and translation files."""

    def __init__(self, *args, **kwargs):
        import inotify.constants

        # extends original gunicorn event mask to monitor metadata changes
        self.event_mask = self.event_mask | inotify.constants.IN_ATTRIB
        super().__init__(*args, **kwargs)

    def run(self):
        self._dirs = self.get_dirs()

        for dirname in self._dirs:
            if os.path.isdir(dirname):
                self._watcher.add_watch(dirname, mask=self.event_mask)

        for event in self._watcher.event_gen():
            if event is None:
                continue

            filename = event[3]
            if filename.endswith((".py", ".env", ".mo")):
                self._callback(filename)


reloader.preferred_reloader = InotifyReloader if reloader.has_inotify else reloader.Reloader
reloader.reloader_engines["auto"] = reloader.preferred_reloader
reloader.reloader_engines["inotify"] = InotifyReloader


def run():
    WSGIApplication("").run()
