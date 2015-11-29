"""Get the base address of the loaded binary"""

import gdb
import re

from pathname import PathName
from mappingparser import MappingsParser

class NotFoundException(Exception):
    def __init__(self, msg):
        super(NotFoundException, self).__init__(msg)

def get_exe():
    info_proc = gdb.execute('info proc', to_string=True)
    for line in info_proc.splitlines():
        match = re.match('^exe = \'(.*)\'$', line)
        if match:
            return match.group(1)
    raise NotFoundException('Error parsing \'info proc\', executable not found.')

class BinBase(gdb.Function):
    """Print the base address of a loaded object (the main executable if none is given)"""
    def __init__(self):
        super(BinBase, self).__init__('base')

    def invoke(self, exe=None):
        exe = exe.string() if exe else get_exe()
        exe = PathName(exe)
        maps = MappingsParser().maps

        for mapping in maps:
            if mapping.pathname and mapping.pathname == exe:
                return mapping.start_addr

        raise NotFoundException('No entry found for {} in /proc/{}/maps'.format(exe, get_pid()))

BinBase()

