#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
import setuptools

def version(package_name):
    with open(os.path.join('src', package_name + '.py'), 'r') as f:
        for line in f.readlines():
            if 'version' in line:
                try:
                    exec(line)
                    assert(isinstance(version, basestring))
                    break
                except (SyntaxError, AssertionError, NameError):
                    pass
    try:
        assert(isinstance(version, basestring))
    except (AssertionError, NameError):
        version = 'unknown'
    return version

def github(owner_name, package_name, version=None):
    # The important things here:
    # 1. The URL should be accessible
    # 2. The URL should point to a page which _is_, or which clearly points _to_, the tarball/zipball/egg
    # 3. The URL should indicate which package and version it is
    return 'http://github.com/{owner_name}/{package_name}/tarball/v{version}#egg={package_name}-{version}'.format(owner_name=owner_name, package_name=package_name, version=version)

def setup():
    owner_name = 'mattbornski'
    package_name = 'shmac'
    setuptools.setup(
        name=package_name,
        version=version(package_name),
        description='Mac-specific shell helpers',
        author=owner_name,
        url='http://github.com/{owner_name}/{package_name}'.format(owner_name=owner_name, package_name=package_name),
        package_dir={'': 'src'},
        py_modules=[
            package_name,
        ],
    )

if __name__ == '__main__':
    setup()