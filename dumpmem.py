"""dump all memory of the process"""

import gdb
from mappingparser import MappingsParser, Mapping

class DumpMem(gdb.Command):
    def __init__(self):
        super(DumpMem, self).__init__('dumpmem', gdb.COMMAND_DATA)
    def invoke(self, argument, from_tty):
        filename = argument
        if filename == '':
            raise Exception("need a filename as argument")
        mappings = MappingsParser().maps
        for mapping in mappings:
            gdb.write('start: {}\n'.format(mapping.start_addr))

DumpMem()

