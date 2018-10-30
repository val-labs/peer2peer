#!/usr/bin/env python
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
setup(name='peer2peer',
      version='2.2.0',
      description='peer 2 peer',
      py_modules=['peer2peer'],
      scripts=['peer2peer/p2pc.py',
               'peer2peer/p2ps.py'],
      install_requires=[
          'gevent-websocket', 'gevent', 'future',
          'leveldb',
          'websocket-client', 'docopt'],
      platforms='any',
      license='MIT')
