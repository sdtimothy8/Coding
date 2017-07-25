# coding=utf-8
# !/usr/bin/env python
"""
Get the source code analysis summary.
"""
import os

if __name__ == "__main__":
    this_dir = os.path.split(os.path.realpath(__file__))[0]
    resultfile = "%s/source_result.log" % this_dir
    # print(resultfile)

    top_dir = os.path.dirname(this_dir)

    file_line_num = 0
    dir_line_num = 0
    all_num = 0
    mod_index = 0

    with open(resultfile, 'w') as outputfile:
        outputfile.write("Start analysis the source code.\n")
        for root, dirs, files in os.walk(top_dir):
            for onedir in dirs:
                if onedir.startswith('.'):
                    print("ignore the dir of %s \n" % onedir)
                    continue
                # process the sub-directory.
                subdirectory = "%s/%s" % (top_dir, onedir)

                for subroot, subdirs, subfiles in os.walk(subdirectory):
                    for filename in subfiles:
                        file_line_num = 0
                        fullpath = os.path.join(subroot, filename)
                        fullpath = fullpath.encode("UTF-8")
                        outputfile.write("%s \n" % fullpath)
        outputfile.write("END")
