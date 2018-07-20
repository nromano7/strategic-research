from contextlib import contextmanager
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

