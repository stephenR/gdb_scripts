import os
import sys

#from longld/peda
exe = os.path.abspath(os.path.expanduser(__file__))
sys.path.append(os.path.dirname(exe))

import binbase
import maps
import dumpmem
