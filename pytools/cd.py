from contextlib import contextmanager
import os

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