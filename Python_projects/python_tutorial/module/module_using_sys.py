#!/usr/bin/python
# *-* coding: utf-8 *-*

import sys

print('The command line arguments are:')
for i in sys.argv:
    print(i)


print '\n\nThe PYTHONPATH is', sys.path, '\n'
