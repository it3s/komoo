import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileModifiedEvent
import subprocess
import os
import re

pwd = os.path.dirname(os.path.abspath(__file__))
PATTERN = r'\d+ tests of \d+ passed, \d+ failed.'


def run_tests_and_notify():

    cmd = 'phantomjs static/tests/run-qunit.js \
               http://localhost:5000/tests/'

    out = subprocess.check_output(cmd, shell=True)
    res = re.search(PATTERN, out).group()

    print out

    failures = int(re.findall('\d+', res)[-1])

    icon = 'dialog-ok' if not failures else 'dialog-error'
    msg = '(JS)    All tests PASSED' if not failures else \
          '(JS)    %s tests FAILED' % failures
    img = os.path.join(pwd, '%s.png' % icon)

    notification = "notify-send --hint int:transient:1 -t 800"
    notification = notification.split() + ['-i', img, msg]
    subprocess.call(notification)


class MdCompileHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if isinstance(event, FileModifiedEvent) \
                and event.src_path.endswith('.js'):
            run_tests_and_notify()

if __name__ == "__main__":
    directory = os.path.abspath('.')
    event_handler = MdCompileHandler()
    observer = Observer()
    observer.schedule(event_handler, path=directory, recursive=True)
    observer.start()

    run_tests_and_notify()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
