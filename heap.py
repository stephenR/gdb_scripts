"""trace allocations"""

import gdb

class HeapFinishBreakpoint(gdb.FinishBreakpoint):
    def __init__(self, tracer, fn_name, args):
        super(HeapFinishBreakpoint, self).__init__(internal=True)
        self._tracer = tracer
        self._fn_name = fn_name
        self._args = args
    def stop (self):
        self._tracer.trace(self._fn_name, self._args, self.return_value)
        return False
    def out_of_scope(self):
        #gdb.write("abnormal finish {}\n".format(self._count))
        pass

class HeapBreakpoint(gdb.Breakpoint):
    def __init__(self, tracer, fn_name):
        super(HeapBreakpoint, self).__init__(fn_name, internal=True)
        self._tracer = tracer
        self._fn_name = fn_name
        self._finish_bp = None
        if fn_name in ['malloc', 'free']:
            self._arg_cnt = 1
        else:
            self._arg_cnt = 2
    def stop(self):
        args = []
        if self._arg_cnt > 0:
            args.append(gdb.parse_and_eval('$rdi'))
        if self._arg_cnt > 1:
            args.append(gdb.parse_and_eval('$rsi'))
        self._finish_bp = HeapFinishBreakpoint(self._tracer, self._fn_name,
                args)
        return False

class HeapTracer(object):
    def __init__(self):
        super(HeapTracer, self).__init__()

    def trace(self, fn_name, args, ret_val):
        def val_to_str(val):
            str_val = str(val)
            try:
                str_val = '0x{:x}'.format(int(str_val))
            except:
                pass
            return str_val
        str_args = map(val_to_str, args)
        output = '{}({})'.format(fn_name, ', '.join(str_args))
        if ret_val is not None:
            output += ' = {}'.format(ret_val)
        gdb.write(output + '\n')

class HeapTracing(gdb.Command):
    def __init__(self):
        super(HeapTracing, self).__init__('heap-tracing-enable',
                gdb.COMMAND_TRACEPOINTS)
        self._enabled = False
        self._tracer = HeapTracer()
        self._breakpoints = []
    def invoke(self, argument, from_tty):
        if self._enabled:
            raise Exception('Heap tracing already enabled')
        for fn_name in ['malloc', 'realloc', 'calloc', 'free']:
            self._breakpoints.append(HeapBreakpoint(self._tracer, fn_name))

HeapTracing()
