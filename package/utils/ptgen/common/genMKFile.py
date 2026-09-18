import os
import StringIO
import debug

tag = 'GenFile'

def genSize_mkFile(file_path, ptgen):
    partSizeCxt = {}

    for part in ptgen.section:
        tmpSize = part.getbSize()
        rawName = part.getABbaseName()
        if part._body['Partition_Name'] != rawName + '_b': # do not print for _b partition, its redundant setting
            # old pattern: BOARD_%sIMAGE_PARTITION_SIZE
            partSizeCxt['TARGET_%s_PARTITION_SIZE'%(rawName.upper())] = tmpSize

    # output
    fp = StringIO.StringIO()
    for key in sorted(partSizeCxt.keys()):
        fp.write('%s:=%s\n'%(key, partSizeCxt[key]))
    genSizeWrite = fp.getvalue()
    fp.close()

    genSizeRead = ''
    if os.path.exists(file_path):
        with open(file_path, 'r') as fp:
            genSizeRead = fp.read()
    if genSizeWrite != genSizeRead:
        with open(file_path, 'w') as fp:
            fp.write(genSizeWrite)
    return #def genSize_iniFile(src_path, tar_path, ptgen):
