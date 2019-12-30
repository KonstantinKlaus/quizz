import hid


def print_usb():
    for d in hid.enumerate():
        keys = list(d.keys())
        for key in keys:
            print("%s : %s" % (key, d[key]))
