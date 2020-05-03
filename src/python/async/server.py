#!/usr/bin/env python3
#
# Simple server to process streaming data throgh TCP connection.
# This is for applying algorithms to streaming data asynchronously.
# This is single-threaded.


import sys as _sys
import time as _tm
import logging as _logging

import asyncio as _asyncio
from functools import partial as _partial

_log = _logging.getLogger(__file__)


__all__ = ['start_server', 'set_preprocessor']


class StreamServer(_asyncio.Protocol):
    """Single-threaded server to receive data from outside."""

    def __init__(self, *, worker=None):
        """Server to process stream data."""
        self._func = lambda d: d
        self._err_hdr = _partial(print, '[ERROR] could not process:', file=_sys.stderr)
        self._verbose = False
        # TODO
        self._worker = worker
        self._n_conn = 0

    def set_preprocessor(self, func, error_handler=None, *args, **kwargs):
        """Set function for preprocessing incoming data.

        Args:
            func: function to apply to incoming data
            error_handler: function
                this will be executed when incoming data can not be applied
                function above
            args, kwargs: arguments for function
        """
        self._func = _partial(func, *args, **kwargs)
        if error_handler is not None:
            self._err_hdr = error_handler

    def connection_made(self, transport):
        if self._verbose:
            peer = transport.get_extra_info('peername')
            print(f'Connection from: {peer}', file=self._fp)
        self._n_conn += 1
        _log.info(f'Current connection: {self._n_conn}')

    def connection_lost(self, ext):
        self._n_conn -= 1
        _log.info(f'Current connection: {self._n_conn}')

    def data_received(self, data):
        """Return data with processing by provided function."""
        data = data.decode().strip()
        if self._verbose:
            print(f'Data received: {data!r}', file=self._fp)

        try:
            processed = self._func(data)

            elapsed = _tm.perf_counter() - self._start
            print(f'[INFO][{elapsed:.4f}] {processed}', file=self._fp)

        except Exception as e:
            self._err_hdr(data)


    async def start_server(self, host, port, *, fp=None, verbose=True):
        """Run server to process data.

        This initially processes incoming data only splitting by ','

        If process data by own function, use `set_preprocessor()`,
        otherwise return the same value directly.

        This has to be run with `asyncio.run()`

        Args:
            host: str
            port: int
            fp: str
                file path. if this is set, save to the file,
                otherwise print to stdout (default: stdout)
            verbose: bool
                show the result verbosely

        Usage:
            >>> pre = lambda x: map(int, x.split(','))
            >>> set_processor(list, pre)
            >>> asyncio.run(start_server(host, port, verbose=True))
            Connection from: ...
            Data received: '0,1'
            [0, 1]
            Data received: '1,2,3,4'
            [1, 2, 3, 4]

        Example:
            Running on local machine with `nc`
                >>> process = lambda x: [val*2 for val in map(int, x.split(','))]
                >>> set_processor(process)
                >>> asyncio.run(start_server('localhost', 3000))

            In another terminal:
                $ nc localhost 3000
                1,2,3,4,5
                11,22,33
                a,b,c

            then, the results on the server will be like following:
                Connection from: ('127.0.0.1', 35526)
                Data received: '1,2,3,4,5'
                [INFO][2.0013] [2, 4, 6, 8, 10]
                Data received: '11,22,33'
                [INFO][4.1885] [22, 44, 66]
                Data received: 'a,b,c'
                [ERROR] could not process: a,b,c
        """
        self._verbose = verbose
        self._start = _tm.perf_counter()
        loop = _asyncio.get_event_loop()

        # set where to write results
        self._fp = fp or _sys.stdout

        server = await loop.create_server(
            lambda: self, host, port
        )

        async with server:
            await server.serve_forever()


class _Worker(object):

    def __init__(self):
        pass

    def set_worker(func, timestep=1, window=None):
        """Set worker function to apply stored data.

        Args:
            func: function to be applied to receved data on server
            timestep: int
                time interval to execute the function in seconds in each step
            window: int
                range to process, if not set process data
                if this is set, process data within the time range.
                For instance, if window=5, process 5 latest data and
                older ones will be discarded.
        """
        # TODO
        pass


_wkr = _Worker()
set_worker = _wkr.set_worker

_svr = StreamServer(worker=_wkr)
set_preprocessor = _svr.set_preprocessor
start_server = _svr.start_server
