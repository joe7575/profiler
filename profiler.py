################################################################################
## profiler.py
################################################################################

# replace:
#     on_timer = foo,
# with:
#     on_timer = function(pos, elapsed) return profiler.profile(1, foo, pos, elapsed) end,

import os, fnmatch, pprint, re, sys

dReferences = {}


def get_lua_files(path):
    lFiles = []
    
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, '*.lua'):
                lFiles.append(os.path.normpath(os.path.join(root, name)))

    return lFiles

    
prog1 = re.compile(r"on_timer *= *function")
prog2 = re.compile(r"on_timer *= *(\w{2,32}),")
prog3 = re.compile(r"on_timer *= *function\(pos, elapsed\) return profiler\.profile\(\d+, (\w{2,32}), pos, elapsed\) end")

def check(fname):
    text = file(fname, "rt").read()
    for result in prog1.finditer(text):
        print "\nInvalid syntax in file ",fname, "!!"

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
    

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print "Syntax: profile.py instrument/deinstrument <path>"
        sys.exit(0)
    if sys.argv[1] == "instrument":
        idx = 0
        for fname in get_lua_files(sys.argv[2]):
            print "File",fname,"...",
            check(fname)
            idx = instrument(fname, idx)
            print "ok"
        gen_reference_file()
    elif sys.argv[1] == "deinstrument":
        idx = 0
        for fname in get_lua_files(sys.argv[2]):
            print "File",fname,"...",
            idx = deinstrument(fname, idx)
            print "ok"
    print idx,"on_timer calls replaced."
    
