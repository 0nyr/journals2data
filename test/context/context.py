import sys
import os

# add the src directory as a base directory
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../../src')))

# need to import that module inside textcase files
# so that they have acces to modules inside the src/ dir
import src