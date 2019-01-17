import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import elastic
from elastic import index, PROJECT_FILES_PATH, PUB_FILES_PATH