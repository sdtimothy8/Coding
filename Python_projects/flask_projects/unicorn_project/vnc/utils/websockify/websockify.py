#!/usr/bin/env python

import websockify
import fcntl
import sys
import os
if __name__ == "__main__":
    try:
        pid_path = sys.path[0] + '/monitor.pid'
        print pid_path
        with open(pid_path, 'r+') as f:
            fcntl.flock(f.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            data = f.read()
            print data
            if int(data) == 0:
                f.write(str(os.getpid()))
            else:
                sys.exit(0)
    except:
        sys.exit(0)
    websockify.websocketproxy.websockify_init()
