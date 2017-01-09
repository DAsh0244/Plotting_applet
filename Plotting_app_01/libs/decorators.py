# -*- coding: utf-8 -*-
import multiprocessing


def process_startup(func):
    """ Debug Decorator for Process Documentation"""
    def printing_wrapper(*args, **kwargs):
        proc = multiprocessing.current_process()
        print('Process started: ' + proc.name)
        print('PROCESS PID: ' + proc.pid)
        return func(*args, **kwargs)
    return printing_wrapper
