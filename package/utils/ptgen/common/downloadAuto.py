import debug

tag = 'downloadAUTO'

#process AUTO flag and add index
def updateVal(pt, arg, download_files, sepcial_operation_type):
    for part in pt.section:
        raw_name = part._body["Partition_Name"]
        if part._body["Download"] == "N":
            part._body['Download_File'] = "NONE"
        elif part._body["Download_File"] == "AUTO":
            if download_files.has_key(raw_name):
                part._body['Download_File'] = download_files[raw_name]
                debug.dbg_print(tag, "%s => %s"%(raw_name, download_files[raw_name]))
            else:
                if part._body['Type'] == "Raw data":
                    part._body['Download_File'] = raw_name.lower() + '.bin'
                else:
                    part._body['Download_File'] = raw_name.lower() + '.img'
        if part._body['Operation_Type'] == 'AUTO':
            if sepcial_operation_type.has_key(raw_name):
                part._body['Operation_Type'] = sepcial_operation_type[raw_name]
            elif part._body['Reserved'] == 'Y':
                part._body['Operation_Type'] = 'RESERVED'
            else:
                if part._body['Download'] == 'N':
                    part._body['Operation_Type'] = 'INVISIBLE'
                else:
                    part._body['Operation_Type'] = 'UPDATE'
