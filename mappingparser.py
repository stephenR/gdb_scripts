import gdb

from pathname import PathName

def get_pid():
    info_proc = gdb.execute('info proc', to_string=True)
    pid_line = info_proc.splitlines()[0]
    return int(pid_line.split(' ')[1])

class Mapping(object):
    def __init__(self, start_addr, end_addr, perms, off, dev, inode, pathname):
        self.start_addr = start_addr
        self.end_addr = end_addr
        self.perms = perms
        self.off = off
        self.dev = dev
        self.inode = inode
        self.pathname = pathname

class MappingsParser(object):
    def __init__(self):
        self.maps = []
        for line in open('/proc/{}/maps'.format(get_pid())):
            self.maps.append(self._parse_line(line))

    def _parse_line(self, line):
            #address           perms offset  dev   inode      pathname  
            line = line.split()
            start, end = map(lambda x: int(x, 16), line[0].split('-'))
            assert(start < end)
            perms, off, dev, inode = line[1:5]
            pathname = ''
            if len(line) > 5:
                pathname = line[5]
            return Mapping(start, end, perms, off, dev, inode, PathName(pathname))

