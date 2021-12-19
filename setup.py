import os
import sys
import re
import subprocess
import shlex

try:
    from setuptools import setup, find_packages
    from setuptools.command.install import install
except ImportError:
    from distutils.core import setup, find_packages
    from distutils.command.install import install


VERSION = '0.6.4'


def get_tag_version():
    cmd = 'git tag --points-at HEAD'
    versions = subprocess.check_output(shlex.split(cmd)).splitlines()
    if not versions:
        return None
    if len(versions) != 1:
        sys.exit(f"Trying to get tag via git: Expected excactly one tag, got {len(versions)}")
    version = versions[0].decode()
    if re.match('^v[0-9]', version):
        version = version[1:]
    return version


class VerifyVersionCommand(install):
    """ Custom command to verify that the git tag matches our version """
    description = 'verify that the git tag matches our version'

    def run(self):
        tag_version = get_tag_version()
        if tag_version and tag_version != VERSION:
            sys.exit(f"Git tag: {tag} does not match the version of this app: {VERSION}")


setup(
    name='websocket_server',
    version=VERSION,
    packages=find_packages("."),
    url='https://github.com/Pithikos/python-websocket-server',
    license='MIT',
    author='Johan Hanssen Seferidis',
    author_email='manossef@gmail.com',
    install_requires=[
    ],
    description='A simple fully working websocket-server in Python with no external dependencies',
    platforms='any',
    cmdclass={
        'verify': VerifyVersionCommand,
    },
    python_requires=">=3.6",
)
