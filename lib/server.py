#!/usr/bin/env python3
# coding:utf-8
# Code forked from Koadic.core.server.py
from socketserver import ThreadingMixIn
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass


class Server(threading.Thread):
    def __init__(self, host, port, handler, session, shell, rc4_key, sleep_time):
        threading.Thread.__init__(self)
        self.daemon = True
        self.handler_class = handler

        self.host = host
        self.port = port
        self.shell = shell
        self.session = session
        self.rc4_key = rc4_key
        self.sleep_time = sleep_time

        self._setup_server()

    def _setup_server(self):
        self.http = ThreadedHTTPServer(
            ('0.0.0.0', self.port), self.handler_class)
        self.http.timeout = None
        self.http.daemon_threads = True
        self.http.host = self.host
        self.http.port = self.port
        self.http.shell = self.shell
        self.http.session = self.session
        self.http.rc4_key = self.rc4_key
        self.http.sleep_time = self.sleep_time

    def run(self):
        try:
            self.http.serve_forever()
        except:
            pass

    def shutdown(self):
        # shut down the server/socket
        self.http.shutdown()
        self.http.socket.close()
        self.http.server_close()
        # self._Thread__stop()

        # make sure all the threads are killed
        for thread in threading.enumerate():
            if thread.isAlive():
                try:
                    thread._Thread__stop()
                except:
                    pass
