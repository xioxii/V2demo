import sys

en_pat = ['env', 'main', 'genPGPT']
def dbg_print(pat, str):
    if len(en_pat) == 0:
        print "[ptgen-py] in %s : %s"%(pat,str)
    return

def ptgen_show(str):
    print "[ptgen-py] %s"%(str)

def dbg_error(pat, str):
    ptgen_show("[ERR] %s : %s"%(pat, str))
    exit(1)
