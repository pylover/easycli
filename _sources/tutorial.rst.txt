Tutorial: Todo List
===================

Let's develop a todo list using ``easycli``.

it's highly recommended to use virtual environment before we continue. I use
`virtualenvwrapper <https://virtualenvwrapper.readthedocs.io/en/latest/>`_.

Create a virtual environment to isolate your hello world application from the 
rest of the system python packages.

.. code-block:: bash

   mkvirtualenv todo


.. code-block:: bash

   workon todo
 

First, we're going to create a classic python module including a
``setup.py`` to be able to install it.


Create a directory named ``todo`` containing a python module named ``todo.py``
:

.. code-block::

   import easycli
   
   
   __version__ = '0.1.0'
   
   
   class Todo(easycli.Root):
       __help__ = 'Simple todo list'
       __arguments__ = [
           easycli.Argument(
               '-v', '--version',
               action='store_true',
               help='Show version'
           ),
       ]
   
       def __call__(self, args):
           if args.version:
               print(__version__)
               return
   
           return super().__call__(args)


And a ``setup.py``:

.. code-block::

   import re
   from os.path import join, dirname
   
   from setuptools import setup
  

   with open(join(dirname(__file__), 'todo.py')) as f:
       version = re.match('.*__version__ = \'(.*?)\'', f.read(), re.S).group(1)
   
   
   dependencies = [
       'easycli',
   ]
   
   
   setup(
       name='todo',
       version=version,
       py_modules=['todo'],
       install_requires=dependencies,
       include_package_data=True,
       license='MIT',
       entry_points={
           'console_scripts': [
               'todo = todo:Todo.quickstart',
           ]
       }
   )


.. note::

   ``setuptools`` offers an argument `entry_points
   <https://setuptools.readthedocs.io/en/latest/setuptools.html#new-and-changed-setup-keywords>`_ 
   which is helpful here.


Then install your project in editable mode:

.. code-block:: bash
   
   cd /path/to/todo
   pip3 install -e .


Test your command line interface with:

.. code-block:: bash

   todo --help

.. code-block:: 

   usage: todo [-h] [-v]
   
   Simple todo list
   
   optional arguments:
     -h, --help     show this help message and exit
     -v, --version  Show version


Test the ``-v/--version`` flag:

.. code-block::

   todo -v
   todo --version


Append Command
^^^^^^^^^^^^^^

``functools`` helps keep our code ``DRY``. Here is how to create a command
to append a line ``list,item`` to a csv file.


.. code-block::

   from os.path import join, dirname
   import functools
   
   
   opendbfile = functools.partial(
       open,
       join(dirname(__file__), 'data.csv')
   )
   
   
   class Append(easycli.SubCommand):
       __command__ = 'append'
       __aliases__ = ['add', 'a']
       __arguments__ = [
           easycli.Argument(
               'list',
               default='',
               help='List name',
           ),
           easycli.Argument(
               'item',
               help='Item name',
           )
       ]
   
       def __call__(self, args):
           with opendbfile('a+') as f:
               f.write(f'{args.list},{args.item}\n')


Add the ``Append`` command class to ``Todo.__arguments__`` collection without 
instantiating it:


.. code-block::

   class Todo(easycli.Root):
       ...
       __arguments__ = [
           ...,
           Append
       ]


Now, see the newly added command (``append`` and it's aliases: ``add,a``) 
in ``-h/--help`` output:

.. code-block::

   todo --help

.. code-block::

   usage: todo [-h] [-v] {append,add,a} ...
   
   Simple todo list
   
   optional arguments:
     -h, --help       show this help message and exit
     -v, --version    Show version
   
   Sub commands:
     {append,add,a}
       append (add, a)


Add an item using:


.. code-block::

   todo append foo bar
   # Or
   todo add foo bar
   # Or
   todo a foo bar


Let's modify our code and use functools to create a reusable 
:class:`.Argument` factory.


.. code-block::

   ListArgument = functools.partial(
       easycli.Argument,
       'list',
       default='',
       help='List name',
   )
   
   
   ItemArgument = functools.partial(
       easycli.Argument,
       'item',
       help='Item name',
   )
   
   
   class Append(easycli.SubCommand):
       ...

       __arguments__ = [
           ListArgument(),
           ItemArgument(),
       ]

       ...


Show Command
^^^^^^^^^^^^

We need a command to show ``lists`` or ``items`` inside a ``list``.


.. code-block::

   def getall(*a, **k):
       with opendbfile(*a, **k) as f:
           for l in f:
               yield l.strip().split(',', 1)


   class Show(easycli.SubCommand):
       __command__ = 'show'
       __aliases__ = ['s', 'l']
       __arguments__ = [
           ListArgument(nargs='?')
       ]
   
       def __call__(self, args):
           if args.list:
               for l, i in getall():
                   if l == args.list:
                       print(i)
   
           else:
               for l, i in getall():
                   print(f'{l}\t{i}')


Add the ``Show`` command class to ``Todo.__arguments__`` collection without 
instantiating it:


.. code-block::

   class Todo(easycli.Root):
       ...
       __arguments__ = [
           ...,
           Append,
           Show
       ]


Test it:

.. code-block::

   todo show 
   todo show foo
   # Or
   todo l
   todo l foo


Delete Command
^^^^^^^^^^^^^^

.. code-block::

   class Delete(easycli.SubCommand):
       __command__ = 'delete'
       __aliases__ = ['d']
       __arguments__ = [
           ListArgument(),
           ItemArgument(),
       ]
   
       def __call__(self, args):
           list_ = args.list
           item = args.item
   
           data = [(l, i) for l, i in getall() if l != list_ or i != item]
           with opendbfile('w') as f:
               for l, i in data:
                   f.write(f'{l},{i}\n')

   ...

   class Todo(easycli.Root):
       ...
       __arguments__ = [
           ...,
           Append,
           Show,
           Delete
       ]


Now, you can add, show and ``delete`` your todo items.

.. code-block::

   todo delete foo bar
   todo d foo bar


Completion
^^^^^^^^^^

I love bash auto completion.

So, the first step to do that is to set the ``__completion__`` class attribute
of the ``Todo`` class.

Thanks to `Argcomplete <https://argcomplete.readthedocs.io/en/latest/index.html#specifying-completers>`_.

.. code-block::

   class Todo(easycli.Root):
       ...
       __completion__ = True
       ...

Take a look at the help message:

.. code-block::

   usage: todo [-h] [-v] {append,add,a,show,s,l,delete,d,completion} ...
   
   Simple todo list
   
   optional arguments:
     -h, --help            show this help message and exit
     -v, --version         Show version
   
   Sub commands:
     {append,add,a,show,s,l,delete,d,completion}
       append (add, a)
       show (s, l)
       delete (d)
       completion          Bash auto completion using argcomplete python package.


As you see the ``completion`` sub command has been added.

.. code-block::

   todo completion --help

.. code-block::

   usage: todo completion [-h] {install,uninstall} ...
   
   optional arguments:
     -h, --help           show this help message and exit
   
   Sub commands:
     {install,uninstall}
       install            Enables autocompletion.
       uninstall          Disables autocompletion.


This is how to enable the bash auto completion

.. code-block::

   todo completion install

After this, to reload and apply changes you need to ``deactivate`` and
``activate`` your virtual env again.

.. code-block::

   # virtualenvwrapper 
   deactivate && workon todo  


Type ``todo`` and hit the ``TAB`` key twice to see the result.

.. code-block::

   $ todo 
   a       append      d         -h        l      show    --version
   add     completion  delete    --help    s      -v 


Dynamic Autocompletion
^^^^^^^^^^^^^^^^^^^^^^

How about implementing autocompletion for ``list`` and or ``items``.

We have to write two functions to get the available lists and items.

.. code-block::

   def listcompleter(prefix, action, parser, parsed_args):
       return set(l for l, _ in getall())
   
   
   def itemcompleter(prefix, action, parser, parsed_args):
       list_ = parsed_args.list
       return list(i for l, i in getall() if l == list_)

Then modify our arguments to use those functions as their completers:

.. code-block::

   ListArgument = functools.partial(
       easycli.Argument,
       'list',
       default='',
       help='List name',
       completer=listcompleter
   )
   
   
   ItemArgument = functools.partial(
       easycli.Argument,
       'item',
       help='Item name',
       completer=itemcompleter
   )


This is the complete version of the ``todo.py``:

.. code-block::

   from os.path import join, dirname
   import functools
   
   import easycli
   
   
   __version__ = '0.1.0'
   
   
   opendbfile = functools.partial(
       open,
       join(dirname(__file__), 'data.csv')
   )
   
   
   def getall(*a, **k):
       with opendbfile(*a, **k) as f:
           for l in f:
               yield l.strip().split(',', 1)
   
   
   def listcompleter(prefix, action, parser, parsed_args):
       return set(l for l, _ in getall())
   
   
   def itemcompleter(prefix, action, parser, parsed_args):
       list_ = parsed_args.list
       return list(i for l, i in getall() if l == list_)
   
   
   ListArgument = functools.partial(
       easycli.Argument,
       'list',
       default='',
       help='List name',
       completer=listcompleter
   )
   
   
   ItemArgument = functools.partial(
       easycli.Argument,
       'item',
       help='Item name',
       completer=itemcompleter
   )
   
   
   class Delete(easycli.SubCommand):
       __command__ = 'delete'
       __aliases__ = ['d']
       __arguments__ = [
           ListArgument(),
           ItemArgument(),
       ]
   
       def __call__(self, args):
           list_ = args.list
           item = args.item
   
           data = [(l, i) for l, i in getall() if l != list_ or i != item]
           with opendbfile('w') as f:
               for l, i in data:
                   f.write(f'{l},{i}\n')
   
   
   class Append(easycli.SubCommand):
       __command__ = 'append'
       __aliases__ = ['add', 'a']
       __arguments__ = [
           ListArgument(),
           ItemArgument(),
       ]
   
       def __call__(self, args):
           with opendbfile('a+') as f:
               f.write(f'{args.list},{args.item}\n')
   
   
   class Show(easycli.SubCommand):
       __command__ = 'show'
       __aliases__ = ['s', 'l']
       __arguments__ = [
           ListArgument(nargs='?')
       ]
   
       def __call__(self, args):
           if args.list:
               for l, i in getall():
                   if l == args.list:
                       print(i)
   
           else:
               for l, i in getall():
                   print(f'{l}\t{i}')
   
   
   class Todo(easycli.Root):
       __help__ = 'Simple todo list'
       __completion__ = True
       __arguments__ = [
           easycli.Argument(
               '-v', '--version',
               action='store_true',
               help='Show version'
           ),
           Append,
           Show,
           Delete
       ]
   
       def __call__(self, args):
           if args.version:
               print(__version__)
               return
   
           return super().__call__(args)


Enjoy your very own todo list.

The complete code is available as a python project on github: 
`easycli-todolist-demo <https://github.com/pylover/easycli-todolist-demo>`_.

