""" 

A module of random code snippets.

Includes:
  timer: a context manager for timing code blocks.
  cd: a context manager for changing the current directory

"""

from contextlib import contextmanager
import os
from time import perf_counter

@contextmanager
def timer(label: str):
  """ 
  A context manager for timing code blocks. 
  
  Usage:

    with timer('label') as t:
      # code block here

  """
  t0 = perf_counter()
  yield 
  t1 = perf_counter()
  print(f'{label} : {t1 - t0} seconds.')

@contextmanager
def cd(destination: str):
  """ 
  A context manager for changing the current directory. 
  cd changes the current directory to the destination 
  directory and reverts back to the original directory 
  after the sub-process has completed. 

  Usage:
  
    with cd('~\some_directory'):
      # sub-process here

  """
  try:
      cwd = os.getcwd()
      os.chdir(destination)
      yield
  finally:
      os.chdir(cwd)


