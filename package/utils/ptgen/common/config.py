import ConfigParser
import debug

tag = 'config'

def read_config(cfg_path, conf):
    iniconf = ConfigParser.ConfigParser()
    iniconf.read(cfg_path)

    # do Layout_csv / AB_Layout parser
    if 'GENERAL' in iniconf.sections():
        debug.dbg_print(tag, "override Layout_csv")
        if 'layout_csv' in iniconf.options('GENERAL'):
            conf['Layout_csv'] = iniconf.get('GENERAL', 'layout_csv')

        debug.dbg_print(tag, "override AB_Layout")
        if 'ab_layout' in iniconf.options('GENERAL'):
            conf['AB_Layout'] = bool(iniconf.get('GENERAL', 'ab_layout') == "True")

    if len(conf['Layout_csv']) > 0:
        debug.ptgen_show('target layout is set and skip platform override settings')
        return

    # do Partition_Exist parser
    if 'Partition_Exist' in iniconf.sections():
        debug.dbg_print(tag, "override Partition_Exist")
        for ent in iniconf.items('Partition_Exist'):
            conf['Partition_Exist'][ent[0]] = ent[1]

    # do Partition_Size_KB parser
    if 'Partition_Size_KB' in iniconf.sections():
        debug.dbg_print(tag, "override Partition_Size_KB")
        for ent in iniconf.items('Partition_Size_KB'):
            conf['Partition_Size_KB'][ent[0]] = ent[1]

def dump_config(conf):
    debug.ptgen_show('*****************Configuration*******************')
    for key,values in  conf.items():
        debug.ptgen_show('%s = %s'%(key,values))
    debug.ptgen_show('*****************Configuration*******************')
