
def import_OrderedDict():
    import sys
    i = sys.version_info
    if i[0] > 2 or i[1] > 6:
        module = 'collections'
    else:
        module = 'trumpet.compat.OrderedDict'
    OD = __import__(module)
    return OD.OrderedDict
