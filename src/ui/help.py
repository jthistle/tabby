
import subprocess
from meta.info import NAME, VERSION, DEV_URL

def get_revision():
    try:
        # File that should be created at distribution time
        from meta.revision import REVISION
    except ImportError:
        rev = subprocess.check_output(["git", "describe", "--always"]).strip().decode("utf-8")
        return rev
    else:
        return REVISION


def get_version():
    return VERSION


HELP_STR = """
=== {name} {version} ===
Revision {rev}

= Keys to change modes while in view mode:

e - enter edit mode
h - display this help message

== Mode-specific bindings

= ALL modes:

esc - back to view mode

= view mode (default):

:   - open console
esc - exit console

= edit mode:

arrow keys        - move cursor
ctrl + arrow keys - move cursor in large steps

---

{name} is by James Thistlewood and is licensed under the GPL-v3.
Development at {url}.
""".format(name=NAME, version=VERSION, rev=get_revision(), url=DEV_URL)
