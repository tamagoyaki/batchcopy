#!/usr/bin/python3
#
# USAGE
#
#   $ cat hoge.csv | ./batchcopy.py
#
#   Don't overwrite if destination exists.
#
#
# FORMAT OF INPUT FILE
#
#    CSV should contain at least 3fields. 'source file', 'command' and
#    'destination directory'. It doesn't care other fields, just ignore.
#
#    For now, available commands are 'copy' and 'ignore'.
#
#    ex)
#      $ cat hoge.csv
#      src/img000.jpg, copy, here/dst,
#      src/readme.txt, copy, there/dst, this is test
#      # this is commnet.
#      tmp/img001.txt, ignore, there/dst, this is test
#
#

import os
import sys
import csv
import shutil

ncmnt = 0
nignr = 0
nblnk = 0
ncopy = 0
nukwn = 0
nexst = 0

for row in csv.reader(sys.stdin, delimiter=','):
    src = ""
    cmd = ""
    dstdir = ""
    ix = 0

    for col in row:
        if 0 == ix:
            src = row[0].strip()
        elif 1 == ix:
            cmd = row[1].strip()
        elif 2 == ix:
            dstdir = row[2].strip()

        ix = ix + 1

    # comment ?
    if src.startswith("#"):
        ncmnt = ncmnt + 1
        continue

    # blank ?
    if "" == src or "" == cmd or "" == dstdir:
        nblnk = nblnk + 1
        continue

    # copy, ignore or unknown
    if "copy" == cmd:
        dstfname = dstdir + "/" + os.path.basename(src)

        # not exist? then make dir
        if not os.path.exists(dstdir):
            os.makedirs(dstdir)

        # not exist? then copy it
        if not os.path.exists(dstfname):
            shutil.copyfile(src, dstfname)
            print("copied: {} -> {}".format(src, dstdir))
            ncopy = ncopy + 1
        else:
            print("exist: {} -> {}".format(src, dstdir))
            nexst = nexst + 1
    elif "ignore" == cmd:
        print("ignored: {} -> {}".format(src, dstdir))
        nignr = nignr + 1
    else:
        print("unknown: {}".format(cmd))
        nukwn = nukwn + 1

    # flush for your preference, maybe it's a bit slow
    sys.stdout.flush()

total = ncopy + nexst + nignr + ncmnt + nblnk + nukwn
print("copied {}, exist {}, ignored {}, "
      "comment {}, blank {}, unknown {}, out of total {}"
      .format(ncopy, nexst, nignr, ncmnt, nblnk, nukwn, total))
