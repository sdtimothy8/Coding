#!/usr/bin/env python
"""
Code Style rule: PEP-8
"""
import os
import subprocess

__author__ = 'shaomingwu@inspur.com'


def launchcmd(cmdstr):
    """
    Launch a cmdstr, and get the result.
    6 June,2015 Edited by Shaomingwu@inspur.com : return the original output data.
    :param cmdstr: command string.
    :return: The result after launching the cmdstr.
    """
    # Check if the input cmdstr is valid?
    pp = subprocess.Popen(cmdstr, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    if pp:
        return pp.stdout


if __name__ == "__main__":
    print("Start checking the source code according to PEP-8.")

    this_dir = os.path.split(os.path.realpath(__file__))[0]
    resultfile = "%s/py_coderule_check.log" % this_dir
    print(resultfile)
    top_dir = os.path.dirname(this_dir)

    # assign the permission for pep8-unicorn.py
    str_chgmod = "chmod a+x %s/pep8_unicorn.py" % this_dir
    cflag = launchcmd(str_chgmod)
    if not cflag:
        print("Failed checking the code style.")
    else:
        cmdpro = "%s/pep8_unicorn.py" % this_dir

        with open(resultfile, 'w') as outputfile:
            for root, dirs, files in os.walk(top_dir):
                for filename in files:
                    if filename in ('manage.py','py_coderule_check.py', 'pep8_unicorn.py'):
                        pass
                    elif filename.endswith(".py"):
                        fullpath = os.path.join(root, filename)
                        # outputfile.write("Checking the source file: %s \n"%fullpath)
                        if root.__contains__("agent/virtlib"):
                            continue
                        if root.__contains__('agent/vnc/'):
                            continue
                        cmdstr = "%s %s"% (cmdpro, fullpath)
                        # print(cmdstr)
                        oneoutput = launchcmd(cmdstr)
                        for oneline in oneoutput:
                            outputfile.write(oneline)
                            print(oneline)



