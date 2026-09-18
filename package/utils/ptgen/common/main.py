import os
import AddrCal
import EnvArg
import downloadAuto
import genMKFile
import genScatter
import genLink
import headerParser
import debug

tag = 'main'

class ptgen:
    def __init__(self, dbg_flag=False):
        """ main class of ptgen """
        self.ptgenList = {}
        self.Used_Size = 0
        self.Version = 4.0
        self.dbg_flag = dbg_flag
        if dbg_flag == True:
            del debug.en_pat[:]

    def setArgs(self, plt_arglist=[]):
        self.ArgList = EnvArg.Arg_Boards()
        EnvArg.parseAndadd(self.ArgList, plt_arglist)

    def computeArgs(self, configs):
        EnvArg.updateVal(self.ArgList, configs)
        #product out
        self.PtgenOut = self.getArgVal('OUT_DIR')
        # set folder for genfile using
        if not os.path.exists(self.PtgenOut):
            os.makedirs(self.PtgenOut)
        return

    def getArgVal(self, name):
        return self.ArgList.argGet(name)

    def setPtgen(self, storage_type = ''):
        """
        # ptgen metadata initial
        """

        if self.ptgenList.has_key(storage_type):
            debug.dbg_error(tag, "%s type is already Init"%(storage_type))
        self.ptgenList[storage_type] = headerParser.LayoutParse_CSV(self.ArgList.argGet('layout_path'), self.ArgList)
        self.ptgenList[storage_type].storage_type = storage_type
        #.log file
        if self.dbg_flag == True:
            debug.dbg_print(tag, "dev_support %s"%(storage_type))
            file_name = '/' + storage_type +'_3_py.log'
            self.ptgenList[storage_type].dbg_p_all("out/" + file_name)

    def run_updateAttr(self, conf):
        for key in self.ptgenList:
            for pt_name, val in conf['Partition_Exist'].items():
                self.ptgenList[key].update(pt_name, 'Default_Exist', val)

            for pt_name, val in conf['Partition_Size_KB'].items():
                self.ptgenList[key].update(pt_name, 'Size_KB', val)

        return

    def run_delEntry(self):
        for key in self.ptgenList:
            # delete some partitions
            self.ptgenList[key].deletebyAttr('Default_Exist', 'N')

            # log file
            if self.dbg_flag == True:
                file_name = '/' + key +'_4_py.log'
                self.ptgenList[key].dbg_p_all("out/" + file_name)

        return #def run_DelRule(self):

    def run_CalAddr(self):
        """
        calculate start_address of partition {Start_Addr} by Byte
        """
        for key in self.ptgenList:
            self.Used_Size = AddrCal.cac_addr(self.ptgenList[key])
            #.log file
            if self.dbg_flag == True:
                file_name = '/' + key +'_7_py.log'
                self.ptgenList[key].dbg_p_all("out/" + file_name)
        return

    def run_updateImg(self, download_files = {}, special_operation_type = {}):
        #download files
        if len(special_operation_type) == 0:
            special_operation_type = {
                'nvram': 'PROTECTED',
                'proinfo': 'PROTECTED',
                'protect1': 'PROTECTED',
                'protect2': 'PROTECTED',
                'flashinfo': 'RESERVED',
            }

        if len(download_files) == 0:
            download_files = {
                'preloader': 'preloader_' + self.getArgVal('MTK_PROJECT') + '.bin',
                'preloader_backup': 'preloader_' + self.getArgVal('MTK_PROJECT') + '.bin',
            }

        for key in self.ptgenList:
            #process AUTO flag and add index
            downloadAuto.updateVal(self.ptgenList[key], self.ArgList, download_files, special_operation_type)
        if self.dbg_flag == True:
            for key in self.ptgenList:
                file_name = '/' + key +'_8_py.log'
                self.ptgenList[key].dbg_p_all("out/" + file_name)

    def genfile_xml(self):
        """
        # generate Scatter xml file.
        """
        file_name = self.PtgenOut + '/' + self.getArgVal('MTK_PLATFORM').upper() + '_openwrt_scatter.xml'
        debug.ptgen_show("Gen xml file in Path %s"%(file_name))
        genScatter.genXML(file_name, self.ptgenList, self.ArgList)

    def genfile_link(self):
        """
        # generate symbol link setup script file.
        """
        file_name = self.PtgenOut + '/setup_link.sh'
        device = self.getArgVal('BOOTING_DEVICE')
        genLink.genScript(file_name, self.ptgenList[device])

    #partition_size.mk
    def genfile_partSize(self):
        """
        # generate partition_size.mk file.
        """
        file_name = self.PtgenOut + '/partition_size.mk'
        device = self.getArgVal('BOOTING_DEVICE')
        debug.ptgen_show("Gen partition_size.mk file in Path %s"%(file_name))
        genMKFile.genSize_mkFile(file_name, self.ptgenList[device])
