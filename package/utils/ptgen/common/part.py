import re
import debug

tag = 'part'

class entry:
    def __init__(self):
        self._body = {}

    def dbg_file_out(self, fp):
        fp.write("{\n")
        for key, value in self._body.items():
            fp.write("    "+ key +"="+value+"\n")
        fp.write("}\n")
        return

    def getABbaseName(self):
        if '_a' in self._body['Partition_Name'] or '_b' in self._body['Partition_Name']:
            return self._body['Partition_Name'][:-2]
        return self._body['Partition_Name']

    def getbSize(self):
        if self._body.has_key('Size_KB'):
            return int(float(self._body['Size_KB']) * 1024)
        else:
            dbg_error(tag, 'partition has no Size_KB')

    def dbg_print(self, str_in):
        print str_in
        for key, val in self._body.items():
            print("%s = %s"%(key, val))

class part_layout:
    """
    part_layout - the main class of ptgen tool
    storage_type [str] the device type that store partition layout
    section      [list] hold all partition entry information
    """
    def __init__(self):
        self.storage_type = ''
        self.section = []

    def update(self, pt_name, attr, val):
        for key in self.section:
            if re.match(pt_name, key._body['Partition_Name']) != None:
                debug.ptgen_show("update attribute %s for %s:%s->%s"%(attr, key._body['Partition_Name'], key._body[attr], val))
                key._body[attr] = val

    def delete(self, pt_name):
        for key in self.section:
            if key._body['Partition_Name'] == pt_name:
                debug.dbg_print(tag, "delete part : %s"%(pt_name))
                self.section.remove(key)

    def deletebyAttr(self, attr, target_val):
        '''
        for key in self.section:
            if key._body[attr] == target_val:
                debug.dbg_print(tag, "delete part : %s"%(key._body['Partition_Name']))
                self.section.remove(key)
        '''
        debug.ptgen_show("delete partition with attr %s=%s"%(attr, target_val))
        self.section = [entry for entry in self.section if entry._body[attr] != target_val]

    def dbg_p_all(self, file_name):
        debug.dbg_print(tag, "dbg_p_all : %s"%(file_name))
        file = open(file_name, 'w')
        for mb in self.section:
            mb.dbg_file_out(file)
        file.close()
        return
