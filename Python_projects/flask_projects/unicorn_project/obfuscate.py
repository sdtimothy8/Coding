#!/usr/bin/env python
"""
Obfuscate the source code.
"""
import os
import commands

__author__ = 'zhangyuanfang@inspur.com'


if __name__ == '__main__':
    this_dir = os.path.split(os.path.realpath(__file__))[0]
    logfile = '%s/obfuscate.log' % this_dir

    with open(logfile, 'w') as outfile:
        outfile.write('Start obfuscate the source code.\n')
        for root, dirs, files in os.walk(this_dir):
            for onedir in dirs:
                if onedir.startswith('.'):
                    continue
                # sub-directory
                subdirectory = '%s/%s' % (this_dir, onedir)

                for subroot, subdirs, subfiles in os.walk(subdirectory):
                    for filename in subfiles:
                        if filename in ('obfuscate.py', 'urls.py', 'configobjftp.py', 'TestSessionAuthticateMiddleWare.py'):
                            pass
                        elif filename.endswith('.py'):
                            fullpath = os.path.join(subroot, filename)
                            outfile.write('    Source file: %s ' % fullpath)
                            # obfuscate the source code
                            obfusput = commands.getoutput('pyobfuscate -r -a -v ' + fullpath)
                            f = open(fullpath, 'w')  # write the result code of obfuscation
                            f.write(obfusput)
                            f.close()
                            outfile.write('obfuscate finished\n')
            break
        outfile.write('All finished !')
