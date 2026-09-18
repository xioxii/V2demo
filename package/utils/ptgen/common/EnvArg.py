import os
import debug

tag = 'Arg'

arg_name_list = [
    'MTK_PLATFORM', 'MTK_PROJECT',
    'BOOTING_DEVICE', 'DEVICE_BLOCK_SIZE',
    'PL_MODE',
    'OUT_DIR',
    'TARGET_CFG_FILE'
]

class Arg_Boards():
    def __init__(self):
        self.unit = {}
        return

    def argInit(self, arg_name_list):
        for name in arg_name_list:
            if name in os.environ:
                self.argSet(name, os.environ[name])
            else:
                debug.dbg_print(tag, '%s is not a os val at parsing time'%(name))

    def argGet(self, name):
        if self.unit.has_key(name):
            return self.unit[name]
        else:
            return '-Non Val-'

    def argSet(self, name, val):
        self.unit[name] = val

    def dbg_print(self):
        debug.ptgen_show('*******************Arguments*********************')
        for key,values in  self.unit.items():
            debug.ptgen_show('%s = %s'%(key,values))
        debug.ptgen_show('*******************Arguments*********************')

def parseAndadd(argList, addition_arg):
    """
    " Add in the addition arguments from the platform
    " addition_arg [in] the platform defined arguments
    " argList     [out] the target arguments list that be added in
    """
    for unit in addition_arg:
        arg_name_list.append(unit)
        dbg_print(tag, "add in new arg %s"%(unit))
    argList.argInit(arg_name_list)

def updateVal(ArgList, configs):
    # parse filepath
    booting_device = ArgList.argGet('BOOTING_DEVICE')
    ab_suffix = ''
    if configs['AB_Layout'] == True:
        ab_suffix = '_ab'

    platform_path = ArgList.argGet('MTK_PLATFORM')
    target_path = os.path.dirname(ArgList.argGet('TARGET_CFG_FILE'))

    # This is for test mode only
    if ArgList.argGet('PL_MODE') != "":
        layout_path = platform_path + "/test_partition_table_internal_" + ArgList.argGet('PL_MODE') + "_emmc.csv"
    # This is for target layout assigned in partition_cfg.ini
    elif len(configs['Layout_csv']) > 0:
        layout_path = target_path + '/' + configs['Layout_csv']
    # This is for no target layout assigned, therefore common platform layout is adopted
    else:
        layout_path = platform_path + "/partition_table_" + booting_device + ab_suffix + ".csv"

    ArgList.argSet('layout_path', layout_path)
    # print all arguments
    ArgList.dbg_print()
    return
