#!/usr/bin/env python

__version_info__ = (0, 1, 2)
__version__ = '.'.join([str(i) for i in __version_info__])
version = __version__

import os.path
import pkg_resources
import shlex
import shutil
import subprocess
import sys
import tempfile

def sudo(command, name=None):
    try:
        # First check to see if we can do this with an existing sudo permission.  Possibly you have already granted it.
        return subprocess.check_call(shlex.split('sudo ' + command))
    except (OSError, subprocess.CalledProcessError):
        # If not, use the Mac sudo dialog to get permission.
        # This is calling out to a third-party binary which is built using ObjectiveC to call the Mac system APIs.
        # The displayed name of the program will be whatever the filename is, believe it or not.
        # Since we let you specify an arbitrary name, it can have spaces in it; the combination of Python
        # subprocess + Mac shell does not like spaces in script names very much, but the find command handles it,
        # which leads us to invoke the script through find instead of directly.
        if name is None:
            name = sys.argv[0] or __name__
        tmpdir = tempfile.mkdtemp()
        try:
            helper = os.path.join(tmpdir, name)
            shutil.copy(pkg_resources.resource_filename(__name__, 'sudo_helper'), helper)
            os.chmod(helper, 0755)
            script = os.path.join(tmpdir, 'script.sh')
            with open(script, 'w') as f:
                f.write('''#!/bin/bash

sudo {command}
'''.format(command=command))
            os.chmod(script, 0755)
            return subprocess.check_call(shlex.split('find {tmpdir} -name "{name}" -exec {} "{script}" \;'.format('{}', tmpdir=tmpdir, name=name, script=script)))
        finally:
            shutil.rmtree(tmpdir)

def sudo_if_necessary(command, *args, **kwargs):
    try:
        return subprocess.check_call(shlex.split(command))
    except (OSError, subprocess.CalledProcessError):
        return sudo(command, *args, **kwargs)