from ipykernel.kernelbase import Kernel
from IPython.core.formatters import DisplayFormatter
from time import sleep
import pandas as pd


def strip_magic(code):
    lines = code.split('\n')
    magic_line = ''
    for i, line in enumerate(lines):
        if line.lstrip().startswith('%'):
            magic_line = line.strip()
            break
    first_line = code.lstrip().split('\n')[0]
    if first_line.startswith('%'):
        magic_code = first_line
        code =code
    return magic_code, code

class EchoKernel(Kernel):
    implementation = 'Echo'
    implementation_version = '1.0'
    language = 'no-op'
    language_version = '0.1'
    language_info = {
        'name': 'Any text',
        'mimetype': 'text/plain',
        'file_extension': '.txt',
    }
    banner = "Echo kernel - as useful as a parrot"

    def __init__(self, **k):
        # connect with kdb
        super().__init__(**k)
        self._formatter = DisplayFormatter()


    def do_execute(self, code, silent, store_history=True, user_expressions=None,
                   allow_stdin=False):
        if not silent:
            magic_code, code = strip_magic(code)
            stream_content = {'name': 'stdout', 'text': str(user_expressions) + '\n'}
            self.send_response(self.iopub_socket, 'stream', stream_content)
            stream_content = {'name': 'stdout', 'text': '===\n'}
            self.send_response(self.iopub_socket, 'stream', stream_content)
            stream_content = {'name': 'stdout', 'text': code}
            self.send_response(self.iopub_socket, 'stream', stream_content)

            o = pd.DataFrame(dict(
                key=list('abc'),
                val=[code] * 3,
            ))

            # stream_content = {'data': {'text/html': '<b>hihihi</b>'},
            #                   'metadata': {}}
            # self.send_response(self.iopub_socket, 'display_data', stream_content)

            data, metadata = self._formatter.format(o)
            stream_content = {
                'data': data,
                'metadata': metadata,
                # 'data': {
                #     'text/html': '<code>bibidi</code>',
                # },
                # 'metadata': {
                # },
                'execution_count': self.execution_count,
            }
            self.send_response(
                self.iopub_socket,
                'execute_result',
                stream_content,
            )

        return {'status': 'ok',
                # The base class increments the execution count
                'execution_count': self.execution_count,
                'payload': [],
                'user_expressions': {},
               }
