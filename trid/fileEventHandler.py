import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class Watcher:

  def __init__(self, directory, log_filepath="./file_log", log_level=None):
    self.observer = Observer()
    self.directory = directory
    
    logging.basicConfig(
      filename=f'{log_filepath}.log', 
      level=logging.DEBUG,
      format='%(levelname)s:%(message)s'
    )
    
  def __enter__(self):
    event_handler = Handler()
    self.observer.schedule(event_handler, self.directory, recursive=True)
    self.observer.start()
    
  def __exit__(self, exc_type=None, exc_val=None, exc_tb=None):
    time.sleep(1)
    self.observer.stop()
    self.observer.join()


class Handler(FileSystemEventHandler):

  @staticmethod
  def on_any_event(event):
    if event.is_directory:
      return None

    elif event.event_type == 'created':
      # Take any action here when a file is first created.
      logging.debug(f"Created - {event.src_path}.")
      # print(f"Created - {event.src_path}.")

    elif event.event_type == 'modified':
      # Taken any action here when a file is modified.
      logging.debug(f"Modified - {event.src_path}.")
      # print(f"Modified - {event.src_path}.")


# with Watcher("."):
#   with open("./test.txt",'w') as f:
#     f.write("")


