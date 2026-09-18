import os
import main
import config
import debug

tag = 'default_ptgen'

class DefaultFlow():
    """ the default ptgen flow """
    configs = {}
    configs['Layout_csv'] = ''
    configs['AB_Layout'] = False
    configs['Partition_Exist'] = {}
    configs['Partition_Size_KB'] = {}

    def __init__(self):
        #init default ptgen class
        self.ptgen = main.ptgen(False)
        self.ptgen.setArgs()

        # TBD: check whether has the platform setting

        # check whether has the project setting
        if os.path.exists(self.ptgen.getArgVal('TARGET_CFG_FILE')):
            config.read_config(self.ptgen.getArgVal('TARGET_CFG_FILE'), self.configs)
            config.dump_config(self.configs)
            debug.dbg_print(tag, "target setting in %s"%(self.ptgen.getArgVal('TARGET_CFG_FILE')))

        self.ptgen.computeArgs(self.configs)

    def run_flow(self):
        debug.ptgen_show("!!!!!!!!!!!!!!!!!!! run_flow %s !!!!!!!!!!!!!!!!!!!"%(self.ptgen.getArgVal('BOOTING_DEVICE')))
        self.ptgen.setPtgen(self.ptgen.getArgVal('BOOTING_DEVICE'))

        self.ptgen.run_updateAttr(self.configs)
        self.ptgen.run_delEntry()
        self.ptgen.run_CalAddr()
        self.ptgen.run_updateImg()

        self.ptgen.genfile_xml()
        self.ptgen.genfile_link()

if __name__ == "__main__":
    debug.ptgen_show("!!!!!!!!!!!!!!!!!!! start !!!!!!!!!!!!!!!!!!!")
    flow = DefaultFlow()
    flow.run_flow()
    debug.ptgen_show("!!!!!!!!!!!!!!!!!!! end !!!!!!!!!!!!!!!!!!!")
