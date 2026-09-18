import csv
import debug
import part as gen

def LayoutParse_CSV(src_path, arg):
    """
    # CSV parsing Rule using to discribe the partition entry inside
    # src_path     [in] source .csv file path
    # arg          [in] arguments that init by setArgs()
    # storage_type [in] emmc , ufs or nand
    """
    # ptgen init
    partLayout = gen.part_layout()
    # CSV file read in
    if src_path != "":
        file = open(src_path, mode='r')
        debug.ptgen_show("partition layout file path : %s"%(src_path))
    else:
        debug.dbg_error("ERR partition layout file lost")

    reader = csv.reader(file)
    layout = []
    for line in reader:
        layout.append(line)

    #parsing header
    header_info = _headerParse(layout[0])

    #parsing entry
    #for i in range(1,len(layout)):
    for entry in layout[1:]:
        partLayout.section.append(_MapRule(header_info, entry))

    return partLayout

def _headerParse(lhd):
    return lhd

def _MapRule(head, entry):
    partEntry = gen.entry()
    partEntry._body = dict(zip(head, entry))
    return partEntry
