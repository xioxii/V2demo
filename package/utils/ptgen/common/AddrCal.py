import debug

tag = 'AddrCalcuate'

# cac_addr - calculate the address of partition layout
# ptgen [in] the partition layout
def cac_addr(ptgen):
    debug.dbg_print(tag, "[cac_addr] storage_type: %s"%(ptgen.storage_type))
    Used_Size = 0

    # Back calcuate
    for idx in range(len(ptgen.section)-1, -1, -1):
        part = ptgen.section[idx]
        if part._body['Reserved'] == 'Y':
            if idx != len(ptgen.section)-1 :
                part._body['Start_Addr'] = str(int(ptgen.section[idx+1]._body['Start_Addr']) + part.getbSize())
            else:
                part._body['Start_Addr'] = str(part.getbSize())

    for idx in range(0, len(ptgen.section)):
        part = ptgen.section[idx]
        st_addr = 0
        if part._body['Reserved'] == 'N':
            if idx != 0 and part._body['Region'] == ptgen.section[idx-1]._body['Region']:
                st_addr = int(ptgen.section[idx-1]._body['Start_Addr']) + ptgen.section[idx-1].getbSize()
                part._body['Start_Addr'] = str(st_addr)
            else:
                part._body['Start_Addr'] = '0'
            part._body['Start_Addr_Text'] = str(hex(int(part._body['Start_Addr'])))
        else:
            part._body['Start_Addr_Text'] = '0xFFFF%04x'%(int(part._body['Start_Addr']) / (128 * 1024))
        Used_Size = Used_Size + float(part._body['Size_KB'])
    debug.dbg_print(tag, "Used_Size=0x%x KB = %d KB =%.2f MB"%(Used_Size, Used_Size, Used_Size/1024))

    return Used_Size# end of cac_addr(ptgen)
