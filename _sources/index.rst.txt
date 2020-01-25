.. easycli documentation master file, created by
   sphinx-quickstart on Tue Jan 21 16:31:18 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to easycli's documentation!
===================================

.. image:: http://img.shields.io/pypi/v/easycli.svg
   :target: https://pypi.python.org/pypi/easycli
 
.. image:: https://travis-ci.org/pylover/easycli.svg?branch=master
   :target: https://travis-ci.org/pylover/easycli

.. image:: https://coveralls.io/repos/github/pylover/easycli/badge.svg?branch=master
   :target: https://coveralls.io/github/pylover/easycli?branch=master

.. image:: https://img.shields.io/badge/Python-%3E%3D3.6-blue
   :target: https://python.org


Just a wrapper arround python ``argparse`` module to easily develop nested
command line applications with autocompletion support like ``git``.


.. code-block::

   from easycli import Root, Argument
   
   
   class MyApp(Root):
       __completion__ = True
       __help__ = '...'
       __arguments__ = [
           Argument('-v', '--version', action='store_true', help='...')
       ]
   
       def __call__(self, args):
           if args.version:
               print('0.1.0')
               return
   
           self._parser.print_help()
   
   
   if __name__ == '__main__':
       MyApp.quickstart()



Contents
********

.. toctree::
   :maxdepth: 2

   tutorial
   apireference


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
