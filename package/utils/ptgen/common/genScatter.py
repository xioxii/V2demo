import os
import StringIO
import debug
from pprint import pprint

tag = 'GenFile'

def _GenHeaderInfo(arg):
    header_info = {}
    header_info['general'] = 'MTK_PLATFORM_CFG'
    header_info['platform'] = arg.argGet('MTK_PLATFORM').upper()
    header_info['project'] = arg.argGet('MTK_PROJECT')
    header_info['config_version'] = 'V2.1.0'

    if arg.argGet('BOOTING_DEVICE') == 'emmc':
        header_info['storage'] = {
            'EMMC': {'boot_channel': 'MSDC_0', 'block_size': hex(512)},
        }
    elif arg.argGet('BOOTING_DEVICE') == 'nand':
        header_info['storage'] = {
            'NAND': {'boot_channel': 'NONE', 'block_size': hex(int(arg.argGet('DEVICE_BLOCK_SIZE')))},
        }
    return header_info


def _ScatterGen(storage_type, ptgen, arg):
    ret_scatter = {}
    for idx in range(len(ptgen.section)):
        part = ptgen.section[idx]
        ret_scatter[part._body['Partition_Name']] = {
            'partition_index': idx,
            'physical_start_addr':part._body['Start_Addr_Text'],
            'linear_start_addr':part._body['Start_Addr_Text'],
            'partition_size':hex(part.getbSize()),
            'file_name':part._body['Download_File'],
            'operation_type':part._body['Operation_Type'],
            'combo_partsize_check':'false'
        }
        # type
        if part._body['Type'] == 'Raw data':
            ret_scatter[part._body['Partition_Name']]['type'] = 'NORMAL_ROM'
        else:
            if arg.argGet('BOOTING_DEVICE') == 'emmc':
                ret_scatter[part._body['Partition_Name']]['type'] = 'EXT4_IMG'
            else:
                ret_scatter[part._body['Partition_Name']]['type'] = 'YAFFS_IMG'
        if part._body['Partition_Name'] == 'preloader':
            ret_scatter[part._body['Partition_Name']]['type'] = 'SV5_BL_BIN'
        if part._body['Partition_Name'] == 'preloader_backup':
            ret_scatter[part._body['Partition_Name']]['type'] = 'SV5_BL_BIN'
        # storage & region
        if storage_type == 'emmc':
            ret_scatter[part._body['Partition_Name']]['storage'] = 'HW_STORAGE_EMMC'
            ret_scatter[part._body['Partition_Name']]['region'] = part._body['Region']
        else:
            ret_scatter[part._body['Partition_Name']]['storage'] = 'HW_STORAGE_NAND'
            ret_scatter[part._body['Partition_Name']]['region'] = 'NONE'
        # is_download
        if part._body['Download'] == 'N':
            ret_scatter[part._body['Partition_Name']]['is_download'] = 'false'
        else:
            ret_scatter[part._body['Partition_Name']]['is_download'] = 'true'
        # is_upgradable
        if part._body['OTA_Update'] == 'N':
            ret_scatter[part._body['Partition_Name']]['is_upgradable'] = 'false'
        else:
            ret_scatter[part._body['Partition_Name']]['is_upgradable'] = 'true'
        # empty_boot_needed
        if part._body['EmptyBoot_Needed'] == 'N':
            ret_scatter[part._body['Partition_Name']]['empty_boot_needed'] = 'false'
        else:
            ret_scatter[part._body['Partition_Name']]['empty_boot_needed'] = 'true'

    return ret_scatter

def genXML(file_name, ptgenList, arg):
    fp = open(file_name, 'w')
    header_info =  _GenHeaderInfo(arg)
    device = arg.argGet('BOOTING_DEVICE')

    fp.write('<?xml version=\"1.0\" encoding=\"utf-8\"?>\n\n')
    fp.write('<root>\n')
    fp.write('  <general name=\"%s\">\n'%(header_info['general']))
    fp.write('    <config_version name=\"%s\">\n'%(header_info['config_version']))
    fp.write('      <platform>%s</platform>\n'%(header_info['platform']))
    fp.write('      <project>%s</project>\n'%(header_info['project']))

    fp.write('    </config_version>\n')
    fp.write('  </general>\n')

    _getXMLscat(device, fp, header_info, ptgenList[device], arg)
    fp.write('</root>\n')
    fp.close()

def _getXMLscat(storage_type, fp, header_info, ptgen, arg):
    pat = {}
    pat['FirstSpaceSymbol'] = "  "
    Scatter_Info = _ScatterGen(storage_type, ptgen, arg)
    fp.write('%s<storage_type name=\"%s\">\n'%(pat['FirstSpaceSymbol'], storage_type.upper()))
    fp.write('%s  <general name=\"MTK_STORAGE_CFG\">\n'%(pat['FirstSpaceSymbol']))
    fp.write('%s    <storage name=\"%s\">\n'%(pat['FirstSpaceSymbol'], storage_type.upper()))
    fp.write('%s      <boot_channel>%s</boot_channel>\n'%(pat['FirstSpaceSymbol'], header_info['storage'][storage_type.upper()]['boot_channel']))
    fp.write('%s      <block_size>%s</block_size>\n'%(pat['FirstSpaceSymbol'], header_info['storage'][storage_type.upper()]['block_size']))
    fp.write('%s    </storage>\n'%(pat['FirstSpaceSymbol']))
    fp.write('%s  </general>\n'%(pat['FirstSpaceSymbol']))
    pat['FirstSpaceSymbol'] = "    "

    for part in ptgen.section:
        pprint(Scatter_Info[part._body['Partition_Name']])
        fp.write('%s<partition_index name=\"SYS%s\">\n'%(pat['FirstSpaceSymbol'], Scatter_Info[part._body['Partition_Name']]['partition_index']))
        fp.write('%s  <partition_name>%s</partition_name>\n'%(pat['FirstSpaceSymbol'], part._body['Partition_Name']))
        fp.write('%s  <file_name>%s</file_name>\n'%(pat['FirstSpaceSymbol'], Scatter_Info[part._body['Partition_Name']]['file_name']))
        fp.write('%s  <is_download>%s</is_download>\n'%(pat['FirstSpaceSymbol'], Scatter_Info[part._body['Partition_Name']]['is_download']))
        fp.write('%s  <type>%s</type>\n'%(pat['FirstSpaceSymbol'], Scatter_Info[part._body['Partition_Name']]['type']))
        fp.write('%s  <linear_start_addr>%s</linear_start_addr>\n'%(pat['FirstSpaceSymbol'], Scatter_Info[part._body['Partition_Name']]['linear_start_addr']))
        fp.write('%s  <physical_start_addr>%s</physical_start_addr>\n'%(pat['FirstSpaceSymbol'], Scatter_Info[part._body['Partition_Name']]['physical_start_addr']))
        fp.write('%s  <partition_size>%s</partition_size>\n'%(pat['FirstSpaceSymbol'], Scatter_Info[part._body['Partition_Name']]['partition_size']))
        fp.write('%s  <region>%s</region>\n'%(pat['FirstSpaceSymbol'], Scatter_Info[part._body['Partition_Name']]['region']))
        fp.write('%s  <storage>%s</storage>\n'%(pat['FirstSpaceSymbol'], Scatter_Info[part._body['Partition_Name']]['storage']))
        fp.write('%s  <operation_type>%s</operation_type>\n'%(pat['FirstSpaceSymbol'], Scatter_Info[part._body['Partition_Name']]['operation_type']))
        fp.write('%s  <is_upgradable>%s</is_upgradable>\n'%(pat['FirstSpaceSymbol'], Scatter_Info[part._body['Partition_Name']]['is_upgradable']))
        fp.write('%s  <empty_boot_needed>%s</empty_boot_needed>\n'%(pat['FirstSpaceSymbol'], Scatter_Info[part._body['Partition_Name']]['empty_boot_needed']))
        fp.write('%s  <combo_partsize_check>%s</combo_partsize_check>\n'%(pat['FirstSpaceSymbol'], Scatter_Info[part._body['Partition_Name']]['combo_partsize_check']))
        fp.write('%s</partition_index>\n'%(pat['FirstSpaceSymbol']))

    pat['FirstSpaceSymbol'] = "  "
    fp.write('%s</storage_type>\n'%(pat['FirstSpaceSymbol']))
