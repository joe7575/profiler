################################################################################
## profiler.py
################################################################################

# replace:
#     on_timer = foo,
# with:
#     on_timer = function(pos, elapsed) return profiler.profile(1, foo, pos, elapsed) end,

import os
import fnmatch
import re
import sys
import zipfile

dReferences = {}


def get_files(path, pattern):
    lFiles = []
    
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                lFiles.append(os.path.normpath(os.path.join(root, name)))

    return lFiles
    
prog1 = re.compile(r"on_timer *= *function")
prog2 = re.compile(r"on_timer *= *(\w{2,32}),")
prog3 = re.compile(r"on_timer *= *function\(pos, elapsed\) return profiler\.profile\(\d+, (\w{2,32}), pos, elapsed\) end")

def check(fname):
    text = file(fname, "rt").read()
    for result in prog1.finditer(text):
        print "\nInvalid syntax in file ",fname, "!!"

def backup(path):
    dest = os.path.normpath(os.path.join(path, "profiler_backup.zip"))
    if not os.path.exists(dest):
        zf = zipfile.ZipFile(dest, "w", zipfile.ZIP_DEFLATED)
        for fname in get_files(path, '*.lua'):
            try:
                zf.write(fname)
            except:
                pass
        print "Backup '%s' created." % dest

def instrument(fname, index):
    data = {"idx": index}

    def repl(matchobj):
        print "replaced",
        templ = r"on_timer = function(pos, elapsed) return profiler.profile(%u, %s, pos, elapsed) end,"
        data["idx"] += 1
        dReferences[data["idx"]] = "%s:%s" % (fname, matchobj.group(1))
        return templ % (data["idx"], matchobj.group(1))
        
    text = file(fname, "rt").read()
    text = prog2.sub(repl, text)
    file(fname, "wt").write(text)
    return data["idx"]

def deinstrument(fname, index):
    data = {"idx": index}

    def repl(matchobj):
        print "replaced",
        data["idx"] += 1
        return r"on_timer = %s" % matchobj.group(1)
        
    text = file(fname, "rt").read()
    text = prog3.sub(repl, text)
    file(fname, "wt").write(text)
    return data["idx"]

def gen_reference_file():
    lOut = ["profiler.lReferences = {"]
    keys = dReferences.keys()
    keys.sort()
    for key in keys:
        lOut.append('  [%u] = "%s",' % (key, dReferences[key]))
    lOut.append("}")
    file("./references.lua", "wt").write("\n".join(lOut))
    
def add_to_depends_txt(path):
    for fname in get_files(sys.argv[2], 'depends.txt'):
        text = file(fname, "rt").read()
        text = "profiler\n" + text
        file(fname, "wt").write(text)

def remove_from_depends_txt(path):
    for fname in get_files(sys.argv[2], 'depends.txt'):
        text = file(fname, "rt").read()
        text = text.replace("profiler\n", "")
        file(fname, "wt").write(text)

def main(cmnd, path):
    if cmnd == "instrument":
        backup(path)
        idx = 0
        for fname in get_files(path, '*.lua'):
            print "File",fname,"...",
            check(fname)
            idx = instrument(fname, idx)
            print "ok"
        gen_reference_file()
        add_to_depends_txt(path)
    elif cmnd == "deinstrument":
        idx = 0
        for fname in get_files(path, '*.lua'):
            print "File",fname,"...",
            idx = deinstrument(fname, idx)
            print "ok"
        remove_from_depends_txt(path)
    print idx,"'on_timer' call(s) replaced."


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print "Syntax: profile.py instrument/deinstrument <path>"
    else:
        main(sys.argv[1], sys.argv[2])
