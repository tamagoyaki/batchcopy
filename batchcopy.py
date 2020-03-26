#!/usr/bin/python3
#
# USAGE
#
#   $ cat hoge.csv | ./batchcopy.py [ options ]
#
#   OPTION:
#
#     --dry-run
#
#
# FORMAT OF INPUT FILE
#
#   CSV should contain at least 2fields. "opcode" and "operand".
#   How many operands required is depending on opcode. for example, opecode
#   "copy" needs 2 operands that are "surce filename" and "distination dir".
#
#
# AVAILABLE OPCODE
#
#    opcode       operand1           operand2          operand3
#    --------+------------------+------------------+------------------+
#    copy      source filename    dist dir           don't care
#    rename    source filename    dist filename      don't care
#    ignore    don't care         don't care         don't care
#
#
# EXAMPLES
#
#      $ cat hoge.csv
#      copy, src/img000.jpg, here/dst,
#      copy, src/readme.txt, there/dst, this is test
#      rename, oldname.csv, newname.csv, "oldname.csv is intact"
#      # this is commnet.
#      ignore, tmp/img001.txt, there/dst, this is test
#
#

import os
import sys
import csv
import shutil


# check commandline options
dryrun = False
for arg in sys.argv[1:]:
    if "--dry-run" == arg:
        dryrun = True
    else:
        print("unknown option: {}".format(arg))
        exit(-1)


def makedirs(dryrun,  name):
    if dryrun is False:
        os.makedirs(name)


def copyfile(dryrun, src, dst):
    if dryrun is False:
        shutil.copyfile(src, dst)


ncmnt = 0
nignr = 0
nlack = 0
ncopy = 0
nrenm = 0
nukwn = 0
nexst = 0

for row in csv.reader(sys.stdin, delimiter=','):
    opc = ""
    opr1 = ""
    opr2 = ""
    ix = 0

    for col in row:
        if 0 == ix:
            opc = row[0].strip()
        elif 1 == ix:
            opr1 = row[1].strip()
        elif 2 == ix:
            opr2 = row[2].strip()

        ix = ix + 1

    # comment ?
    if opr1.startswith("#"):
        ncmnt = ncmnt + 1
        continue

    # blank ?
    if "" == opc or "" == opr1 or "" == opr2:
        nlack = nlack + 1
        continue

    # execute command
    if "copy" == opc:
        dstfname = opr2 + "/" + os.path.basename(opr1)

        # not exist? then make dir
        if not os.path.exists(opr2):
            makedirs(dryrun, opr2)

        # not exist? then copy it
        if not os.path.exists(dstfname):
            copyfile(dryrun, opr1, dstfname)

            print("copied: {} -> {}".format(opr1, opr2))
            ncopy = ncopy + 1
        else:
            print("exist: {} -> {}".format(opr1, opr2))
            nexst = nexst + 1
    elif "rename" == opc:
        dstfname = opr2
        dirname = os.path.dirname(dstfname)

        # not exist? then make dir
        if "" != dirname:
            if not os.path.exists(dirname):
                makedirs(dryrun, dirname)

        # not exist? then rename it (source stays intact)
        if not os.path.exists(dstfname):
            copyfile(dryrun, opr1, dstfname)
            print("renamed: {} -> {}".format(opr1, opr2))
            nrenm = nrenm + 1
        else:
            print("exist: {} -> {}".format(opr1, opr2))
            nexst = nexst + 1
    elif "ignore" == opc:
        print("ignored: {} -> {}".format(opr1, opr2))
        nignr = nignr + 1
    else:
        print("unknown: {}".format(opc))
        nukwn = nukwn + 1

    # flush for your preference, maybe it's a bit slow
    sys.stdout.flush()


# status report
total = ncopy + nexst + nignr + ncmnt + nlack + nukwn
message = "copied {}, exist {}, ignored {}," \
          "comment {}, blank {}, unknown {}, total {}" \
          .format(ncopy, nexst, nignr, ncmnt, nlack, nukwn, total)
if dryrun is True:
    message = message + " (DRY RUN)"

print(message)
