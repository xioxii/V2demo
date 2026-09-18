import os
import re
import debug

tag = 'GenFile'

def genScript(fname, ptgenList):
    with open(fname, 'w') as fp:
        fp.write('mkdir -p /dev/block\n')
        if ptgenList.storage_type == 'emmc':
            pname_list = [part._body['Partition_Name'] for part in ptgenList.section if part._body['Region'] == 'EMMC_USER']
            ab_basename_list = [re.match('^(.+)_[ab]$', pname).group(1) for pname in pname_list if re.match('^(.+)_[ab]$', pname) != None]
            debug.ptgen_show("setup link file for %s"%(pname_list[1:-1]))
            for name in pname_list[1:-1]:
                fp.write('ln -s /dev/mmcblk0p%d /dev/block/%s\n'%(pname_list.index(name), name))

            if len(ab_basename_list) != 0:
                ab_basename_unique = list(set(ab_basename_list))
                ab_basename_unique.sort(key = ab_basename_list.index)

                debug.ptgen_show("setup link file for active slot %s"%(ab_basename_unique))
                fp.write('active_slot=$(cat /proc/cmdline | grep -E \"bootslot=([^ ]+)\" -o | awk -F \'=\' \'{print $2}\')\n')
                fp.write('ab_list="%s"\n'%(' '.join(ab_basename_unique)))
                fp.write('for basename in ${ab_list}\n')
                fp.write('do\n')
                fp.write('    ln -s /dev/block/${basename}_${active_slot} /dev/block/${basename}\n')
                fp.write('done\n')
        elif ptgenList.storage_type == 'nand':
            fp.write('mkdir -p /dev/mtd\n')
            pname_list = [part._body['Partition_Name'] for part in ptgenList.section if part._body['Region'] == 'NAND_USER']
            dw_file_list = [part._body['Download_File'] for part in ptgenList.section if part._body['Region'] == 'NAND_USER']
            ab_basename_list = [re.match('^(.+)_[ab]$', pname).group(1) for pname in pname_list if re.match('^(.+)_[ab]$', pname) != None]
            debug.ptgen_show("setup link file for %s"%(pname_list[1:-1]))
            addon=0
            for name in pname_list[1:-1]:
                fp.write('ln -s /dev/mtd%d /dev/mtd/%s\n'%(pname_list.index(name)+addon, name))
                fp.write('ln -s /dev/mtdblock%d /dev/block/%s\n'%(pname_list.index(name)+addon, name))
                if dw_file_list[pname_list.index(name)] == 'root.squashfs':
                    addon=1

            if len(ab_basename_list) != 0:
                ab_basename_unique = list(set(ab_basename_list))
                ab_basename_unique.sort(key = ab_basename_list.index)

                debug.ptgen_show("setup link file for active slot %s"%(ab_basename_unique))
                fp.write('active_slot=$(cat /proc/cmdline | grep -E \"bootslot=([^ ]+)\" -o | awk -F \'=\' \'{print $2}\')\n')
                fp.write('ab_list="%s"\n'%(' '.join(ab_basename_unique)))
                fp.write('for basename in ${ab_list}\n')
                fp.write('do\n')
                fp.write('    ln -s /dev/mtd/${basename}_${active_slot} /dev/mtd/${basename}\n')
                fp.write('    ln -s /dev/block/${basename}_${active_slot} /dev/block/${basename}\n')
                fp.write('done\n')
        else:
            debug.ptgen_show('Not support link file generation for %s yet'%(ptgenList.storage_type))

    os.chmod(fname, 0755)
