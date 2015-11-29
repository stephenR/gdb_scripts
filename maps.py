"""Print /proc/self/maps"""

import gdb

def get_pid():
    info_proc = gdb.execute('info proc', to_string=True)
    pid_line = info_proc.splitlines()[0]
    return int(pid_line.split(' ')[1])

class Maps(gdb.Command):
    def __init__(self):
        super(Maps, self).__init__('maps', gdb.COMMAND_STATUS)
    def invoke(self, argument, from_tty):
        with open('/proc/{}/maps'.format(get_pid())) as fd:
            gdb.write(fd.read())

Maps()
