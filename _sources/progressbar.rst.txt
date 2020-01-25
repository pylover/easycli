ProgressBar
===========

.. code-block::

   from easycli import ProgressBar 
  

   with ProgressBar(100) as p:
       for i in range(100):
           ...  # do slow job
           p.increment()


